import smtplib
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import logging
import json
import zipfile

logger = logging.getLogger(__name__)

def load_email_config(config_path):
    """加载邮件配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载邮件配置文件失败: {e}")
        return None


def create_zip_report(source_dir, output_filename):
    """打包目录为 ZIP 文件"""
    try:
        with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=os.path.dirname(source_dir))
                    zipf.write(file_path, arcname)
        return output_filename
    except Exception as e:
        logger.error("打包报告失败: %s", e, exc_info=True)
        return None

def send_email_report(email_config):
    """发送测试报告邮件"""
    if not isinstance(email_config, dict):
        logger.error("邮件配置应为字典类型")
        return

    try:
        # 获取 allure_output 目录路径
        report_dir = email_config.get('report_path', '')
        if not report_dir or not os.path.isfile(report_dir):
            report_dir = os.path.dirname(report_dir)

        allure_output_dir = os.path.abspath('../allure_output')  # 新的统一报告目录

        # 创建 ZIP 文件路径
        zip_path = os.path.join(os.path.dirname(report_dir), 'allure_full_report.zip')

        # 打包 allure_output 目录
        zip_file = create_zip_report(allure_output_dir, zip_path)

        sender = SendEmail(
            host=email_config['host'],
            port=email_config.get('port', 465),
            user=email_config['user'],
            password=email_config['password']
        )

        if zip_file and os.path.exists(zip_file):
            content = "<h3>测试已完成，请查收压缩包中的完整测试报告（含原始数据和index.html报告）</h3>"
        else:
            content = "<h3>测试已完成，未找到测试报告文件</h3>"
            zip_file = None

        sender.send_email(
            subject='自动化测试报告',
            content=content,
            filename=zip_file,
            to_addrs=email_config['to_addrs']
        )
        logger.info("测试报告邮件已发送")
    except Exception as e:
        logger.error("发送邮件失败: %s", e, exc_info=True)

class SendEmail:
    """发送邮件"""

    def __init__(self, host, user, password, port=465):
        """
        :param host: smtp server address
        :param port: smtp server report
        :param user: Email account number
        :param password: SMTP service authorization code of mailbox
        """
        if port == 465 or port == 587:
            self.smtp = smtplib.SMTP_SSL(host=host, port=port)
        else:
            self.smtp = smtplib.SMTP(host=host, port=port)
        self.smtp.ehlo()
        self.smtp.login(user=user, password=password)
        self.user = user

    def send_email(self, subject="test report", content=None, filename=None, to_addrs=None):
        """
        :param subject: Email subject
        :param content: Email content
        :param filename: Attachment document
        :param to_addrs: Addressee's address
        :type to_addrs: str or list
        :return:
        """
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = self.user
        if isinstance(to_addrs, str):
            msg["To"] = to_addrs
        elif to_addrs and isinstance(to_addrs, list):
            msg["To"] = to_addrs[0]
        if not content:
            content = time.strftime("%Y-%m-%d-%H_%M_%S") + ":测试报告"
        text = MIMEText(content, _subtype="html", _charset="utf8")
        msg.attach(text)
        if filename and os.path.isfile(filename):
            with open(filename, "rb") as f:
                content = f.read()
            try:
                report = MIMEApplication(content, _subtype=None)
            except:
                report = MIMEApplication(content)
            name = os.path.split(filename)[1]
            report.add_header('content-disposition', 'attachment', filename=name)
            msg.attach(report)
        try:
            self.smtp.send_message(msg, from_addr=self.user, to_addrs=to_addrs)
        except Exception as e:
            logger.error("Failed to send test report: %s", e)
            raise
        else:
            logger.info("The test report has been sent")

logger = logging.getLogger(__name__)


def load_email_config(config_path):
    """加载邮件配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载邮件配置文件失败: {e}")
        return None


def send_test_report(email_config):
    """使用 SendEmail 类发送测试报告"""
    if not isinstance(email_config, dict):
        logger.error("邮件配置应为字典类型")
        return

    try:
        # 初始化 SendEmail 实例
        sender = SendEmail(
            host=email_config['host'],
            user=email_config['user'],
            password=email_config['password'],
            port=email_config.get('port', 465)
        )

        # 构建邮件内容
        subject = '自动化测试报告'
        content = """
        <p>测试已完成，请查收附件中的测试报告。</p>
        <p>此邮件由自动化系统发出，请勿回复。</p>
        """

        # 添加附件
        filename = email_config.get('report_path')

        # 收件人处理
        to_addrs = email_config.get('to_addrs', [])

        # 发送邮件
        sender.send_email(subject=subject, content=content, filename=filename, to_addrs=to_addrs)
    except Exception as e:
        logger.error("发送邮件失败: %s", e, exc_info=True)
