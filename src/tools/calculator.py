"""
计算器工具示例 - 展示工具的基本结构
"""
import re


def calculator(expression: str) -> str:
    """
    简单的计算器工具，用于执行基础数学运算

    Args:
        expression: 数学表达式，如 "23 + 45" 或 "100 * 2"

    Returns:
        计算结果或错误信息
    """
    try:
        # 清理输入，只保留数字和运算符
        cleaned = re.sub(r'[^0-9+\-*/().\s]', '', expression)

        if not cleaned:
            return "Error: 无效的数学表达式"

        # 安全计算（eval 在这里只处理清理后的数学表达式）
        result = eval(cleaned)

        return f"计算结果: {result}"

    except ZeroDivisionError:
        return "Error: 除数不能为零"
    except Exception as e:
        return f"Error: 计算出错 - {str(e)}"


def get_current_time() -> str:
    """
    获取当前时间的工具

    Returns:
        当前日期和时间字符串
    """
    from datetime import datetime
    now = datetime.now()
    return f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}"
