from openai import OpenAI
from typing import List, Dict
import os


def ask(messages: List[Dict], model: str = None, temperature: float = 0):
    """
    调用 LLM API

    Args:
        messages: 消息列表
        model: 模型名称，默认从环境变量读取
        temperature: 温度参数，控制随机性

    Returns:
        API 响应对象
    """
    # 从环境变量读取配置，如果没有则使用默认值
    api_key = os.getenv('OPENAI_API_KEY', '')
    base_url = os.getenv('OPENAI_BASE_URL', 'https://coding.dashscope.aliyuncs.com/v1')
    model = model or os.getenv('DEFAULT_MODEL', 'qwen3.5-plus')

    if not api_key:
        raise ValueError("请设置 OPENAI_API_KEY 环境变量或在 .env 文件中配置")

    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messages
    )

    return response


        