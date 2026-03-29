from ..llm import ask
def Cot():
    print('COT:')
    #  给LLM一个 role
    system_prompt = "You are a helpful assistant" 

    question = """
    Q: The cafeteria had 23 apples.
    If they used 20 to make lunch and bought 6 more, how many apples do they have?
    A:"""

    # 对输入的 messages 进行处理，以满足 LLM 对输入的要求
    messages = [
        {"role":"system", "content":system_prompt},
        {"role":"user", "content":question},
    ]


    response = ask(messages)

    # 后处理返回的结果
    print(response.choices[0].message.content)


