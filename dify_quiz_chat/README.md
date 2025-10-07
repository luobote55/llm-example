# Dify交互式选择题聊天应用

基于Dify API开发的交互式选择题生成和答题系统。用户输入任何学习主题，AI将自动生成相应的选择题，并提供实时答题和评分功能。

## 功能特点

- 🎯 **智能题目生成**：基于Dify AI，根据用户输入的主题自动生成选择题
- 🎮 **交互式答题**：点击选项即可答题，实时显示正确/错误状态
- 📊 **实时评分**：自动计算得分，提供学习反馈
- 🎨 **美观界面**：现代化的Web界面，支持响应式设计
- 🔧 **灵活配置**：支持不同难度级别（简单、中等、困难）

## 技术栈

- **后端**：FastAPI + Python
- **前端**：HTML5 + CSS3 + JavaScript + Bootstrap 5
- **AI服务**：Dify API
- **部署**：支持Docker部署

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <your-repo-url>
cd dify_quiz_chat

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp env.example .env

# 编辑.env文件，填入你的Dify API配置
DIFY_API_KEY=your_dify_api_key_here
DIFY_BASE_URL=https://api.dify.ai/v1
```

### 3. 运行应用

```bash
# 启动应用
python app.py

# 或者使用uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 访问应用

打开浏览器访问：http://localhost:8000

## 使用说明

1. **输入主题**：在输入框中输入任何学习主题，如"Python编程"、"中国历史"、"数学"等
2. **选择难度**：选择题目难度（简单、中等、困难）
3. **生成题目**：点击"生成题目"按钮，AI将为你生成相应的选择题
4. **答题**：点击你认为正确的选项
5. **查看结果**：系统会显示正确答案和详细解释，并更新你的得分

## API接口

### 生成选择题

```http
POST /api/generate-quiz
Content-Type: application/json

{
    "topic": "Python编程",
    "difficulty": "medium",
    "question_count": 1,
    "user_id": "user123"
}
```

### 提交答案

```http
POST /api/submit-answer
Content-Type: application/json

{
    "question_id": "q_1_1234",
    "selected_answer": "A",
    "user_id": "user123"
}
```

## Docker部署

```bash
# 构建镜像
docker build -t dify-quiz-chat .

# 运行容器
docker run -d -p 8000:8000 --env-file .env dify-quiz-chat
```

## 项目结构

```
dify_quiz_chat/
├── app.py              # 主应用文件
├── requirements.txt    # Python依赖
├── env.example        # 环境变量模板
├── README.md          # 项目说明
├── templates/         # HTML模板
│   └── index.html     # 主页面
└── static/           # 静态文件（可选）
```

## 配置说明

### Dify API配置

1. 在Dify平台创建应用
2. 获取API Key
3. 配置API Base URL（通常是 `https://api.dify.ai/v1`）

### 环境变量

- `DIFY_API_KEY`: Dify API密钥
- `DIFY_BASE_URL`: Dify API基础URL
- `APP_HOST`: 应用监听地址（默认：0.0.0.0）
- `APP_PORT`: 应用端口（默认：8000）
- `DEBUG`: 调试模式（默认：True）

## 扩展功能

### 数据库集成

当前版本使用内存存储，生产环境建议集成数据库：

```python
# 示例：使用SQLite
import sqlite3

def init_database():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id TEXT PRIMARY KEY,
            topic TEXT,
            question TEXT,
            options TEXT,
            correct_answer TEXT,
            explanation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
```

### 用户系统

可以添加用户认证和答题历史记录：

```python
# 示例：用户答题历史
def save_user_answer(user_id, question_id, selected_answer, is_correct):
    # 保存用户答题记录
    pass

def get_user_statistics(user_id):
    # 获取用户统计信息
    pass
```

## 故障排除

### 常见问题

1. **Dify API连接失败**
   - 检查API Key是否正确
   - 确认网络连接正常
   - 验证Dify服务状态

2. **题目生成失败**
   - 检查提示词格式
   - 确认AI返回的JSON格式正确
   - 查看应用日志

3. **前端显示异常**
   - 检查浏览器控制台错误
   - 确认静态文件路径正确
   - 验证JavaScript语法

### 日志查看

```bash
# 查看应用日志
tail -f app.log

# 或使用uvicorn日志
uvicorn app:app --log-level debug
```

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue或联系开发者。
