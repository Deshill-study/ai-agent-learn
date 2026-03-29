from openai import OpenAI
from typing import List, Dict

def ask(messages: List[Dict]):
        #需要指定api key 以及base_url
        client = OpenAI(api_key='', base_url="https://coding.dashscope.aliyuncs.com/v1")
        response = client.chat.completions.create(
                model = 'qwen3.5-plus',
                temperature = 0,
                messages = messages
        )
        
        return response


        