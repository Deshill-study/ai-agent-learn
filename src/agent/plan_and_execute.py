from ..llm import ask
def plan():
    # thanks to langchain

    plan_system_prompt = """
        Let's first understand the problem and devise a plan to solve the problem.
        Please output the plan starting with the header 'Plan:' and then followed by a numbered list of steps. 
        Please make the plan the minimum number of steps required to accurately complete the task. If the task is a question, 
        the final step should almost always be 'Given the above steps taken, please respond to the users original question'. 
    """

    # user content
    question = 'the population gap between Toronto and New York city'

    # messages
    messages = [
        {'role':'system', 'content': plan_system_prompt},
        {'role':'user', 'content': question}
    ]
    response = ask(messages)

    plans = response.choices[0].message.content
    print(plans)
