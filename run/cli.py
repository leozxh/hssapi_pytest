# 导入 argparse 模块，用于解析命令行参数
import argparse
from custom_runner import run_tests  # 替换为实际运行测试的模块
from common.email_utils import send_email_report
import json

# 定义 main 函数，作为程序的入口点
def main():
    # 创建 ArgumentParser 对象，用于解析命令行参数
    parser = argparse.ArgumentParser(description="许愿狐接口自动化测试工具")
    
    # 添加 --no-email 参数，当使用该参数时，值为 True，表示不发送测试报告邮件
    parser.add_argument("--no-email", action="store_true", help="不发送测试报告邮件")

    # 解析命令行参数，并将结果存储在 args 变量中
    args = parser.parse_args()

    # 运行测试
    run_tests()

    # 如果没有 --no-email 参数，则发送邮件
    if not args.no_email:
        # 加载邮件配置
        email_config_path = "../data/email_config.json"
        with open(email_config_path, 'r', encoding='utf-8') as f:
            email_config = json.load(f)
        # 发送邮件报告
        send_email_report(email_config)
    else:
        print("[INFO] 邮件发送已跳过")

# 检查是否直接运行该脚本，如果是，则调用 main 函数
if __name__ == "__main__":
    main()