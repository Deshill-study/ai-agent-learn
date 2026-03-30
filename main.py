from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

from src.agent.plan_and_execute import plan_and_execute

# 运行 Plan and Execute 示例
plan_and_execute()
