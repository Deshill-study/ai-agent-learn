# AI Agent Learn

本项目基于 Tallisgo/llm_based_agent 二次开发，遵循 MIT License。

一个用于学习和实践多种 AI Agent 模式的 Python 项目，实现了 Chain of Thought、Refine、Plan and Execute 等经典 Agent 模式。

## 项目结构

```
.
├── main.py                      # 主入口文件
├── requirements.txt             # 依赖文件
├── src/
│   ├── agent/                   # Agent 模式实现
│   │   ├── cot.py              # Chain of Thought 模式
│   │   ├── plan_and_execute.py # Plan and Execute 模式
│   │   ├── refine.py           # Refine 自我改进模式
│   │   └── react.py            # ReAct 模式（待实现）
│   ├── llm/                     # LLM 接口
│   │   └── llm.py              # 大语言模型调用封装
│   └── tools/                   # 工具集
│       ├── calculator.py       # 计算器和获取时间工具
│       └── web_search.py       # 联网搜索工具
```

## 安装依赖

```bash
pip install -r requirements.txt
```

依赖包括：
- `openai` - OpenAI API 客户端
- `duckduckgo_search` - DuckDuckGo 搜索
- `beautifulsoup4` - HTML 解析
- `python-dotenv` - 环境变量管理

## 配置

在项目根目录创建 `.env` 文件，配置你的 API 密钥：

```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=your_base_url_here  # 可选，用于第三方 API 代理
```

## Agent 模式说明

### 1. Chain of Thought (CoT)

链式思考模式，让 AI 展示逐步推理过程。

**原理**：通过让模型"一步步思考"，提高复杂问题的解决准确率。

**示例**：数学应用题解答

```python
from src.agent.cot import Cot
Cot()
```

### 2. Refine

自我改进模式，通过迭代优化提升输出质量。

**工作流程**：
1. 初始生成（如翻译初稿）
2. 反思检查（找出可改进之处）
3. 根据反馈重新生成（优化后的翻译）

**示例**：翻译优化

```python
from src.agent.refine import Refine
Refine()
```

### 3. Plan and Execute

计划与执行模式，由 LLM 自主制定计划并调用工具执行。

**工作流程**：
1. **Planning**: LLM 制定执行计划
2. **Execution**: LLM 自主控制执行，通过 Thought/Action 循环调用工具
3. **Final Answer**: 根据执行结果生成最终答案

**特点**：
- LLM 自主决定何时调用工具
- 支持 ReAct 风格的 Thought/Action 循环
- 内置最大步数限制（max_steps=10）防止无限循环

**可用工具**：
- `calculator(expression)` - 执行数学计算
- `get_current_time()` - 获取当前时间

**运行示例**：

```python
python main.py
```

或直接运行：

```python
from src.agent.plan_and_execute import plan_and_execute
plan_and_execute()
```

### 4. ReAct (待实现)

ReAct 模式结合推理（Reasoning）与行动（Acting）。

**循环流程**：
- Think（思考）
- Act（行动）
- Observe（观察）
- ...循环直到完成任务

## 工具使用

### 联网搜索

```python
from src.tools.web_search import internet_search

results = internet_search("人工智能最新发展")
```

### 计算器工具

```python
from src.tools.calculator import calculator, get_current_time

# 数学计算
result = calculator("(23 + 45) * 2")

# 获取当前时间
time = get_current_time()
```

## 提示词基础

项目中的提示词分为系统提示词和用户提示词：

```python
# 系统提示词 - 定义 AI 身份和行为
system_prompt = "You are a helpful assistant"

# 用户提示词 - 具体任务需求
user_prompt = "请计算 23 + 45 的结果"

# 构造消息
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]
```

## 参考资源

- [langchain](https://github.com/langchain-ai/langchain) - Plan and Execute 参考
- [translation-agent](https://github.com/andrewyng/translation-agent) - Refine 模式参考
- [ReAct Paper](https://arxiv.org/abs/2210.03629) - ReAct 模式论文
