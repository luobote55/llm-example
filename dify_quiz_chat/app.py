#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dify交互式选择题聊天应用
输入题目，返回交互式选择题
"""

import os
import json
import httpx
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = FastAPI(title="Dify Quiz Chat", description="基于Dify的交互式选择题聊天应用")

# 静态文件和模板配置
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dify配置
DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_BASE_URL = os.getenv("DIFY_BASE_URL", "https://api.dify.ai/v1")
print("dify 配置：", DIFY_API_KEY, DIFY_BASE_URL)

class QuizRequest(BaseModel):
    """选择题请求模型"""
    topic: str
    difficulty: str = "medium"  # easy, medium, hard
    question_count: int = 1
    user_id: str = "default_user"

class QuizResponse(BaseModel):
    """选择题响应模型"""
    question: str
    options: List[str]
    correct_answer: str
    explanation: str
    question_id: str

class AnswerRequest(BaseModel):
    """答案提交请求模型"""
    question_id: str
    selected_answer: str
    user_id: str

class AnswerResponse(BaseModel):
    """答案验证响应模型"""
    is_correct: bool
    correct_answer: str
    explanation: str
    score: int

class DifyQuizGenerator:
    """Dify选择题生成器"""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.conversation_id = ""
        
    async def generate_quiz(self, topic: str, difficulty: str = "medium", question_count: int = 1) -> List[QuizResponse]:
        """生成选择题"""
        if not self.api_key or not self.base_url:
            raise HTTPException(status_code=500, detail="Dify配置未正确设置")
        
        # 构建提示词
        prompt = self._build_quiz_prompt(topic, difficulty, question_count)
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat-messages",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "inputs": {},
                        "query": prompt,
                        "response_mode": "blocking",
                        "conversation_id": self.conversation_id,
                        "user": "quiz_generator"
                    }
                )
                
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail=f"Dify API错误: {response.text}")
                
                result = response.json()
                self.conversation_id = result.get("conversation_id", "")
                
                # 解析AI返回的选择题
                quiz_data = self._parse_quiz_response(result.get("answer", ""))
                return quiz_data
                
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"请求错误: {str(e)}")
    
    def _build_quiz_prompt(self, topic: str, difficulty: str, question_count: int) -> str:
        """构建选择题生成提示词"""
        difficulty_map = {
            "easy": "简单",
            "medium": "中等", 
            "hard": "困难"
        }
        
        prompt = f"""
请根据主题"{topic}"生成{question_count}道{difficulty_map.get(difficulty, "中等")}难度的选择题。

要求：
1. 每道题包含题目、4个选项（A、B、C、D）、正确答案和详细解释
2. 题目要有一定的挑战性，但不要过于简单或困难
3. 选项要合理，包含干扰项
4. 解释要详细，说明为什么选择这个答案

请严格按照以下JSON格式返回：

```json
{{
    "questions": [
        {{
            "question": "题目内容",
            "options": {{
                "A": "选项A内容",
                "B": "选项B内容", 
                "C": "选项C内容",
                "D": "选项D内容"
            }},
            "correct_answer": "A",
            "explanation": "详细解释为什么选择这个答案"
        }}
    ]
}}
```

请确保返回的是有效的JSON格式，不要包含其他内容。
"""
        return prompt
    
    def _parse_quiz_response(self, response_text: str) -> List[QuizResponse]:
        """解析AI返回的选择题数据"""
        try:
            # 提取JSON部分
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("未找到有效的JSON格式")
            
            json_str = response_text[start_idx:end_idx]
            data = json.loads(json_str)
            
            questions = []
            for i, q in enumerate(data.get("questions", [])):
                options = [q["options"]["A"], q["options"]["B"], q["options"]["C"], q["options"]["D"]]
                
                quiz_response = QuizResponse(
                    question=q["question"],
                    options=options,
                    correct_answer=q["correct_answer"],
                    explanation=q["explanation"],
                    question_id=f"q_{i+1}_{hash(q['question']) % 10000}"
                )
                questions.append(quiz_response)
            
            return questions
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # 如果解析失败，返回一个示例题目
            return [QuizResponse(
                question="基础问题（解析失败，返回示例）",
                options=["选项A", "选项B", "选项C", "选项D"],
                correct_answer="A",
                explanation="这是一个示例题目，请检查AI返回的格式是否正确。",
                question_id="sample_1"
            )]

# 初始化Dify生成器
quiz_generator = DifyQuizGenerator(DIFY_API_KEY, DIFY_BASE_URL)

# 存储题目和答案（实际应用中应使用数据库）
quiz_storage = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """主页"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/generate-quiz", response_model=List[QuizResponse])
async def generate_quiz(request: QuizRequest):
    """生成选择题"""
    try:
        questions = await quiz_generator.generate_quiz(
            topic=request.topic,
            difficulty=request.difficulty,
            question_count=request.question_count
        )
        
        # 存储题目到内存中（实际应用中应使用数据库）
        for question in questions:
            quiz_storage[question.question_id] = {
                "correct_answer": question.correct_answer,
                "explanation": question.explanation,
                "topic": request.topic
            }
        
        return questions
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/submit-answer", response_model=AnswerResponse)
async def submit_answer(request: AnswerRequest):
    """提交答案并验证"""
    if request.question_id not in quiz_storage:
        raise HTTPException(status_code=404, detail="题目不存在")
    
    stored_data = quiz_storage[request.question_id]
    is_correct = request.selected_answer.upper() == stored_data["correct_answer"].upper()
    
    # 计算分数（简单示例）
    score = 10 if is_correct else 0
    
    return AnswerResponse(
        is_correct=is_correct,
        correct_answer=stored_data["correct_answer"],
        explanation=stored_data["explanation"],
        score=score
    )

@app.get("/api/quiz-history")
async def get_quiz_history(user_id: str = "default_user"):
    """获取答题历史"""
    # 这里应该从数据库获取历史记录
    return {"message": "答题历史功能待实现", "user_id": user_id}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
