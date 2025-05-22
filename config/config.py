import os
from common.common_utils import CommonUtils

ENV = 'test'  # 可选: test, pre, prod

# 加载 DOMAIN 配置
domain_config = CommonUtils.read_env_config(section='domain', key=ENV)
# 如果 domain_config 是字符串（不是字典），直接赋值给当前环境
if isinstance(domain_config, str):
    DOMAINS = {
        ENV: domain_config
    }
else:
    # 否则按字典处理
    DOMAINS = {
        'test': domain_config.get('test', ''),
        'pre': domain_config.get('pre', ''),
        'prod': domain_config.get('prod', '')
    }


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录

DATA_PATH = {
    'test_cases': os.path.join(BASE_DIR, 'data', 'testcases.xlsx')
}


REPORT_CONFIG = {
    "report_dir": os.path.join(BASE_DIR, "reports"),
    "title": "许愿狐接口测试报告",
    "tester": "zxh",
    "desc": "包含登录和智能商单等操作",
    "template": 1
}

EMAIL_CONFIG_PATH = os.path.join(BASE_DIR, "data", "email_config.json")