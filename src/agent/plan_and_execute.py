"""
Plan and Execute 模式
工作流程：
1. Planning: LLM 制定一个执行计划
2. Execution: 由 LLM 自主决定如何调用工具执行计划
3. Final Answer: 根据执行结果给出最终答案

示例任务: "计算 (23 + 45) * 2 的结果，然后告诉我当前时间"
"""
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

from ..llm import ask
from ..tools.calculator import calculator, get_current_time


# 可用工具注册表
AVAILABLE_TOOLS = {
    "calculator": calculator,
    "get_current_time": get_current_time
}


def execute_tool(tool_name: str, tool_input: str):
    """
    执行指定的工具

    Args:
        tool_name: 工具名称
        tool_input: 工具输入参数

    Returns:
        工具执行结果
    """
    if tool_name not in AVAILABLE_TOOLS:
        return f"错误: 未知工具 '{tool_name}'"

    tool_func = AVAILABLE_TOOLS[tool_name]
    try:
        if tool_input and tool_input.strip():
            result = tool_func(tool_input)
        else:
            result = tool_func()
        return result
    except Exception as e:
        return f"错误: {str(e)}"


def plan_and_execute():
    """
    Plan and Execute 模式的完整实现
    执行阶段由 LLM 自主决定如何调用工具
    """
    print("=" * 50)
    print("Plan and Execute 模式示例")
    print("=" * 50)

    # ========== Step 1: Planning 阶段 ==========
    print("\n【Step 1】制定执行计划...")
    print("-" * 40)

    # 用户任务
    task = "计算 (23 + 45) * 2 的结果，然后告诉我当前时间"
    print(f"任务: {task}\n")

    # 告诉 LLM 有哪些可用工具
    tools_description = """
可用工具:
1. calculator(expression) - 执行数学计算，参数为数学表达式如 "23 + 45"
2. get_current_time() - 获取当前时间，无需参数
"""

    plan_system_prompt = f"""你是一个任务规划助手。请分析用户任务，制定详细的执行计划。

{tools_description}

请输出一个执行计划，格式如下:
Plan:
1. [步骤描述] - 使用工具: [工具名] 或 无需工具
2. [步骤描述] - 使用工具: [工具名] 或 无需工具
...

确保计划覆盖所有必要步骤，每一步要明确是否需要使用工具以及使用哪个工具。
"""

    messages = [
        {"role": "system", "content": plan_system_prompt},
        {"role": "user", "content": f"请为以下任务制定执行计划:\n{task}"}
    ]

    response = ask(messages)
    plan = response.choices[0].message.content
    print(f"生成的计划:\n{plan}\n")

    # ========== Step 2: Execution 阶段 (由 LLM 自主执行) ==========
    print("【Step 2】由 LLM 自主执行计划...")
    print("-" * 40)

    execution_results = []

    # 构建执行阶段的系统提示
    execute_system_prompt = f"""你是一个任务执行助手。根据制定的计划，你需要逐步执行任务。

{tools_description}

你的任务是根据计划和已执行步骤的结果，决定下一步需要做什么。

对于每一步，请输出以下格式:
Thought: [你的思考过程，分析当前状态和下一步该做什么]
Action: [工具名] | [工具参数] 或 Action: 完成 | [最终答案]

注意:
- 如果还需要调用工具，使用 "Action: 工具名 | 参数" 格式
- 如果任务已完成，使用 "Action: 完成 | 最终答案内容" 格式
- 工具参数如果是数学表达式，请确保格式正确
"""

    # 构建执行对话历史
    execute_messages = [
        {"role": "system", "content": execute_system_prompt},
        {"role": "user", "content": f"任务: {task}\n\n计划:\n{plan}\n\n请开始执行，输出 Thought 和 Action。"}
    ]

    max_steps = 10  # 防止无限循环
    step = 0

    while step < max_steps:
        step += 1
        print(f"\n> 执行步骤 {step}:")

        # 调用 LLM 决定下一步
        response = ask(execute_messages)
        llm_output = response.choices[0].message.content
        print(f"  LLM 输出:\n{llm_output}")

        # 解析 Thought 和 Action
        thought = ""
        action = ""
        action_input = ""

        for line in llm_output.split('\n'):
            line = line.strip()
            if line.startswith('Thought:'):
                thought = line.replace('Thought:', '').strip()
            elif line.startswith('Action:'):
                action_part = line.replace('Action:', '').strip()
                if '|' in action_part:
                    action, action_input = action_part.split('|', 1)
                    action = action.strip()
                    action_input = action_input.strip()
                else:
                    action = action_part

        # 检查是否完成
        if action == "完成":
            print(f"\n  ✅ 执行完成!")
            execution_results.append(f"最终结果: {action_input}")
            break

        # 执行工具调用
        if action and action in AVAILABLE_TOOLS:
            tool_result = execute_tool(action, action_input)
            print(f"  工具调用: {action}('{action_input}')")
            print(f"  执行结果: {tool_result}")
            execution_results.append(f"步骤{step}: 使用 {action}({action_input}) -> {tool_result}")

            # 将结果反馈给 LLM
            execute_messages.append({"role": "assistant", "content": llm_output})
            execute_messages.append({
                "role": "user",
                "content": f"上一步执行结果: {tool_result}\n\n请继续下一步，输出 Thought 和 Action。"
            })
            print('现在的execute_messages为')
            print(execute_messages)
        elif action and action not in AVAILABLE_TOOLS:
            error_msg = f"错误: 未知工具 '{action}'"
            print(f"  {error_msg}")
            execute_messages.append({"role": "assistant", "content": llm_output})
            execute_messages.append({
                "role": "user",
                "content": f"{error_msg}\n可用工具: {list(AVAILABLE_TOOLS.keys())}\n请重新思考并输出 Thought 和 Action。"
            })
        else:
            print(f"  未能解析 Action，继续执行...")
            break

    # ========== Step 3: Final Answer 阶段 ==========
    print("\n【Step 3】生成最终答案...")
    print("-" * 40)

    # 构建最终回答的上下文
    context = "\n".join(execution_results)

    final_system_prompt = """你是一个结果汇总助手。根据执行步骤的结果，生成一个清晰、友好的最终答案。
请综合所有信息，以自然的方式回答用户的问题。"""

    final_user_prompt = f"""原始任务: {task}

执行过程和结果:
{context}

请生成最终答案:"""

    messages = [
        {"role": "system", "content": final_system_prompt},
        {"role": "user", "content": final_user_prompt}
    ]

    response = ask(messages)
    final_answer = response.choices[0].message.content

    print(f"\n✅ 最终答案:\n{final_answer}\n")
    print("=" * 50)


def plan():
    """仅制定计划的简化版本（保留原有功能）"""
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
        {'role': 'system', 'content': plan_system_prompt},
        {'role': 'user', 'content': question}
    ]
    response = ask(messages)

    plans = response.choices[0].message.content
    print(plans)


if __name__ == "__main__":
    plan_and_execute()
