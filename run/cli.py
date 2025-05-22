# 导入 argparse 模块，用于解析命令行参数
import argparse

# 从 run.runner 模块中导入 run_all 函数，该函数可能用于运行所有测试
from runner import run_all

# 定义 main 函数，作为程序的入口点
def main():
    # 创建 ArgumentParser 对象，用于解析命令行参数
    parser = argparse.ArgumentParser(description="许愿狐接口自动化测试工具")
    
    # 添加 --no-email 参数，当使用该参数时，值为 True，表示不发送测试报告邮件
    parser.add_argument("--no-email", action="store_true", help="不发送测试报告邮件")

    # 解析命令行参数，并将结果存储在 args 变量中
    args = parser.parse_args()

    # TODO: 根据参数控制是否发送邮件
    # 这里需要根据 args.no_email 的值来决定是否发送邮件
    # 如果 args.no_email 为 True，则不发送邮件；否则发送邮件
    run_all()

# 检查是否直接运行该脚本，如果是，则调用 main 函数
if __name__ == "__main__":
    main()