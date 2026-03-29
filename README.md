本项目基于 Tallisgo/llm_based_agent 二次开发，遵循 MIT License。


# 提示词  
提示词又分为系统提示词和用户提示词，系统提示词定义了ai的身份，用户提示词说明具体的需求
```
plan_system_prompt = """
    Let's first understand the problem and devise a plan to solve the problem.
    Please output the plan starting with the header 'Plan:' and then followed by a numbered list of steps. 
    Please make the plan the minimum number of steps required to accurately complete the task. If the task is a question, 
    the final step should almost always be 'Given the above steps taken, please respond to the users original question'. 
"""

# user content
question = 'the population gap between Toronto and New York city'

# messages为列表，然后里面放字典
messages = [
    {'role':'system', 'content': plan_system_prompt},
    {'role':'user', 'content': question}
]
```


# 工具
### 联网搜索工具
```
from ddgs import DDGS
def internet_search(query: str):
    with DDGS() as ddgs:
        # 删掉了过期参数 backend='api'，自动用最新模式
        ddgs_gen = ddgs.text(
            query,
            max_results=5, 
            region="wt-wt", 
            safesearch="moderate", 
            timelimit="y"
        )
        if ddgs_gen:
            return [r for r in ddgs_gen]
    return "No results found."
```

# COT：
chain of thought，让ai展示思考过程，一步步思考推理
# Refine
就是自我修改，比如：翻译文本A->检查可以提升的地方->根据检查结果重新翻译一遍
# plan_and_execute

# react
ReAct 模式 AI Agent  
Think（思考）  
Act（行动）  
Observe（观察）  
Think…  
