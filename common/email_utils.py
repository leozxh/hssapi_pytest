import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import json

logger = logging.getLogger(__name__)


def load_email_config(config_path):
    """加载邮件配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载邮件配置文件失败: {e}")
        return None


def send_email_report(email_config_path):
    """发送测试报告邮件"""
    email_config = load_email_config(email_config_path)
    if not email_config:
        logger.error("邮件配置加载失败，无法发送邮件")
        return

    try:
        # 创建邮件内容
        msg = MIMEMultipart()
        msg['From'] = email_config['user']
        msg['To'] = ', '.join(email_config['to_addrs'])
        msg['Subject'] = '自动化测试报告'

        # 邮件正文
        body = "测试已完成，请查收附件中的测试报告。"
        msg.attach(MIMEText(body, 'plain'))

        # 添加 HTML 报告附件（可选）
        report_path = email_config.get('report_path')
        if report_path and os.path.exists(report_path):
            with open(report_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            html_part = MIMEText(html_content, 'html')
            html_part.add_header('Content-Disposition', 'attachment', filename='report.html')
            msg.attach(html_part)

        # 发送邮件
        with smtplib.SMTP(email_config['host'], email_config['port']) as server:
            server.login(email_config['user'], email_config['password'])
            server.sendmail(email_config['user'], email_config['to_addrs'], msg.as_string())

        logger.info("测试报告邮件已发送")

    except Exception as e:
        logger.error("发送邮件失败: %s", e)
