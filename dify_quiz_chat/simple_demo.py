#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dify交互式选择题聊天应用 - 简化演示版本
不依赖外部库，可以直接运行
"""

import json
import os
from typing import Dict, List, Any

class SimpleQuizGenerator:
    """简化的选择题生成器"""
    
    def __init__(self):
        self.quiz_templates = {
            "Python编程": [
                {
                    "question": "Python中哪个关键字用于定义函数？",
                    "options": ["function", "def", "define", "func"],
                    "correct_answer": "B",
                    "explanation": "在Python中，使用'def'关键字来定义函数。"
                },
                {
                    "question": "以下哪个是Python的内置数据类型？",
                    "options": ["list", "array", "vector", "matrix"],
                    "correct_answer": "A", 
                    "explanation": "list是Python的内置数据类型，用于存储有序的元素集合。"
                }
            ],
            "中国历史": [
                {
                    "question": "中国历史上第一个统一的封建王朝是？",
                    "options": ["夏朝", "商朝", "秦朝", "汉朝"],
                    "correct_answer": "C",
                    "explanation": "秦朝是中国历史上第一个统一的封建王朝，由秦始皇建立。"
                },
                {
                    "question": "中国古代四大发明不包括？",
                    "options": ["造纸术", "指南针", "火药", "印刷术"],
                    "correct_answer": "D",
                    "explanation": "中国古代四大发明是造纸术、指南针、火药和印刷术。"
                }
            ],
            "数学": [
                {
                    "question": "2的3次方等于多少？",
                    "options": ["6", "8", "9", "12"],
                    "correct_answer": "B",
                    "explanation": "2的3次方 = 2 × 2 × 2 = 8"
                },
                {
                    "question": "圆的面积公式是？",
                    "options": ["πr²", "2πr", "πd", "πr"],
                    "correct_answer": "A",
                    "explanation": "圆的面积公式是πr²，其中r是半径。"
                }
            ]
        }
    
    def generate_quiz(self, topic: str, difficulty: str = "medium") -> List[Dict]:
        """生成选择题"""
        # 查找匹配的主题
        for key, questions in self.quiz_templates.items():
            if topic.lower() in key.lower() or key.lower() in topic.lower():
                return questions[:1]  # 返回第一道题作为示例
        
        # 如果没有匹配的主题，返回通用题目
        return [{
            "question": f"关于{topic}的基础问题",
            "options": ["选项A", "选项B", "选项C", "选项D"],
            "correct_answer": "A",
            "explanation": f"这是一个关于{topic}的示例题目。"
        }]

class SimpleQuizChat:
    """简化的选择题聊天应用"""
    
    def __init__(self):
        self.generator = SimpleQuizGenerator()
        self.score = 0
        self.total_questions = 0
    
    def display_welcome(self):
        """显示欢迎信息"""
        print("🎯 Dify交互式选择题聊天应用 - 演示版")
        print("=" * 50)
        print("输入任何学习主题，AI将为你生成相应的选择题")
        print("支持的主题示例：Python编程、中国历史、数学等")
        print("输入 'quit' 或 'exit' 退出程序")
        print("=" * 50)
    
    def display_question(self, question_data: Dict, question_num: int):
        """显示题目"""
        print(f"\n📝 题目 {question_num}:")
        print(f"   {question_data['question']}")
        print("\n选项：")
        
        options = question_data['options']
        for i, option in enumerate(options):
            print(f"   {chr(65 + i)}. {option}")
        
        return options
    
    def get_user_answer(self) -> str:
        """获取用户答案"""
        while True:
            answer = input("\n请选择你的答案 (A/B/C/D): ").strip().upper()
            if answer in ['A', 'B', 'C', 'D']:
                return answer
            elif answer in ['QUIT', 'EXIT']:
                return 'QUIT'
            else:
                print("❌ 请输入有效的选项 (A/B/C/D)")
    
    def check_answer(self, question_data: Dict, user_answer: str) -> bool:
        """检查答案"""
        correct_answer = question_data['correct_answer']
        is_correct = user_answer == correct_answer
        
        if is_correct:
            print("✅ 回答正确！")
            self.score += 10
        else:
            print(f"❌ 回答错误。正确答案是：{correct_answer}")
        
        print(f"\n💡 解释：{question_data['explanation']}")
        return is_correct
    
    def display_score(self):
        """显示得分"""
        print(f"\n🏆 当前得分：{self.score} / {self.total_questions * 10}")
        if self.total_questions > 0:
            percentage = (self.score / (self.total_questions * 10)) * 100
            print(f"📊 正确率：{percentage:.1f}%")
    
    def run(self):
        """运行聊天应用"""
        self.display_welcome()
        
        while True:
            # 获取用户输入
            topic = input("\n🎯 请输入学习主题: ").strip()
            
            if topic.lower() in ['quit', 'exit', '退出']:
                print("\n👋 感谢使用！再见！")
                break
            
            if not topic:
                print("❌ 请输入有效的主题")
                continue
            
            # 生成题目
            print(f"\n🤖 正在为你生成关于'{topic}'的选择题...")
            questions = self.generator.generate_quiz(topic)
            
            if not questions:
                print("❌ 无法生成题目，请尝试其他主题")
                continue
            
            # 显示并答题
            for i, question_data in enumerate(questions, 1):
                self.total_questions += 1
                options = self.display_question(question_data, i)
                
                user_answer = self.get_user_answer()
                if user_answer == 'QUIT':
                    print("\n👋 感谢使用！再见！")
                    return
                
                self.check_answer(question_data, user_answer)
                self.display_score()
            
            # 询问是否继续
            continue_choice = input("\n🔄 是否继续生成新题目？(y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes', '是', '继续']:
                print("\n👋 感谢使用！再见！")
                break

def main():
    """主函数"""
    try:
        app = SimpleQuizChat()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 程序被中断，再见！")
    except Exception as e:
        print(f"\n❌ 程序出现错误: {e}")

if __name__ == "__main__":
    main()
