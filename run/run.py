import json
from custom_runner import run_tests
from common.email_utils import send_email_report  # 新增导入发送邮件方法

# 邮件配置路径和报告路径
EMAIL_CONFIG_PATH = "../data/email_config.json"

if __name__ == '__main__':
    # 1. 运行测试并生成 allure 结果
    try:
        run_tests()
    except Exception as e:
        print(f"[ERROR] 测试运行失败: {e}")
    # 2. 更新 email_config.json 中的 report_path（可选）

    with open(EMAIL_CONFIG_PATH, 'r', encoding='utf-8') as f:
        email_config = json.load(f)

    # 3. 发送邮件报告
    send_email_report(email_config)