#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dify Quiz Chat 应用测试脚本
"""

import asyncio
import httpx
import json
from app import DifyQuizGenerator

async def test_quiz_generation():
    """测试选择题生成功能"""
    print("🧪 开始测试选择题生成功能...")
    
    # 模拟Dify API响应
    mock_response = {
        "conversation_id": "test_conv_123",
        "answer": '''
```json
{
    "questions": [
        {
            "question": "Python中哪个关键字用于定义函数？",
            "options": {
                "A": "function",
                "B": "def",
                "C": "define",
                "D": "func"
            },
            "correct_answer": "B",
            "explanation": "在Python中，使用'def'关键字来定义函数。这是Python的语法规则。"
        }
    ]
}
```
'''
    }
    
    # 创建生成器实例
    generator = DifyQuizGenerator("test_key", "https://api.dify.ai/v1")
    
    # 测试解析功能
    questions = generator._parse_quiz_response(mock_response["answer"])
    
    print(f"✅ 成功解析 {len(questions)} 道题目")
    
    for i, question in enumerate(questions, 1):
        print(f"\n📝 题目 {i}:")
        print(f"   问题: {question.question}")
        print(f"   选项: {question.options}")
        print(f"   正确答案: {question.correct_answer}")
        print(f"   解释: {question.explanation}")
        print(f"   题目ID: {question.question_id}")
    
    return questions

async def test_api_endpoints():
    """测试API端点"""
    print("\n🌐 开始测试API端点...")
    
    base_url = "http://localhost:8000"
    
    try:
        async with httpx.AsyncClient() as client:
            # 测试主页
            print("📄 测试主页...")
            response = await client.get(f"{base_url}/")
            if response.status_code == 200:
                print("✅ 主页访问成功")
            else:
                print(f"❌ 主页访问失败: {response.status_code}")
            
            # 测试生成题目API
            print("🎯 测试生成题目API...")
            quiz_data = {
                "topic": "Python编程",
                "difficulty": "medium",
                "question_count": 1,
                "user_id": "test_user"
            }
            
            response = await client.post(
                f"{base_url}/api/generate-quiz",
                json=quiz_data,
                timeout=30.0
            )
            
            if response.status_code == 200:
                questions = response.json()
                print(f"✅ 成功生成 {len(questions)} 道题目")
                
                if questions:
                    question = questions[0]
                    print(f"   题目: {question['question']}")
                    print(f"   选项: {question['options']}")
                    
                    # 测试提交答案API
                    print("📝 测试提交答案API...")
                    answer_data = {
                        "question_id": question["question_id"],
                        "selected_answer": "A",
                        "user_id": "test_user"
                    }
                    
                    response = await client.post(
                        f"{base_url}/api/submit-answer",
                        json=answer_data
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        print("✅ 答案提交成功")
                        print(f"   是否正确: {result['is_correct']}")
                        print(f"   正确答案: {result['correct_answer']}")
                        print(f"   得分: {result['score']}")
                    else:
                        print(f"❌ 答案提交失败: {response.status_code}")
                        print(f"   错误信息: {response.text}")
            else:
                print(f"❌ 生成题目失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
                
    except httpx.ConnectError:
        print("❌ 无法连接到服务器，请确保应用正在运行")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")

def test_quiz_logic():
    """测试选择题逻辑"""
    print("\n🔍 测试选择题逻辑...")
    
    # 测试题目解析
    test_response = '''
```json
{
    "questions": [
        {
            "question": "以下哪个是Python的内置数据类型？",
            "options": {
                "A": "list",
                "B": "array",
                "C": "vector",
                "D": "matrix"
            },
            "correct_answer": "A",
            "explanation": "list是Python的内置数据类型，用于存储有序的元素集合。"
        }
    ]
}
```
'''
    
    generator = DifyQuizGenerator("test", "test")
    questions = generator._parse_quiz_response(test_response)
    
    if questions and len(questions) > 0:
        question = questions[0]
        print("✅ 题目解析成功")
        print(f"   问题: {question.question}")
        print(f"   选项数量: {len(question.options)}")
        print(f"   正确答案: {question.question_id}")
        
        # 测试答案验证逻辑
        correct_answer = question.correct_answer
        test_answers = ["A", "B", "C", "D"]
        
        for answer in test_answers:
            is_correct = answer.upper() == correct_answer.upper()
            print(f"   答案 {answer}: {'✅ 正确' if is_correct else '❌ 错误'}")
    else:
        print("❌ 题目解析失败")

async def main():
    """主测试函数"""
    print("🚀 开始Dify Quiz Chat应用测试")
    print("=" * 50)
    
    # 测试选择题逻辑
    test_quiz_logic()
    
    # 测试题目生成
    await test_quiz_generation()
    
    # 测试API端点（需要应用运行）
    print("\n" + "=" * 50)
    print("💡 提示：要测试API端点，请先启动应用：")
    print("   python app.py")
    print("   然后运行：python test_app.py --api")
    
    import sys
    if "--api" in sys.argv:
        await test_api_endpoints()
    
    print("\n🎉 测试完成！")

if __name__ == "__main__":
    asyncio.run(main())
