import random
import string
import sys
import time
import json
from datetime import datetime
import openpyxl
import configparser
import os

class CommonUtils:
    @staticmethod
    def add_project_root_to_path():
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

    @staticmethod
    def generate_random_number():
        random_str = random.randint(100, 10000)
        return random_str

    @staticmethod
    def generate_random_delivery_day():
        """
        随机生成 deliveryDay 值，范围为 [7, 15, 30, 60, 90, 120]
        :return: int
        """
        return random.choice([7, 15, 30, 60, 90, 120])

    @staticmethod
    def get_current_timestamp():
        """
        获取当前时间的时间戳（秒级）
        :return: 秒级时间戳
        """
        return int(time.mktime(datetime.now().timetuple()))

    @staticmethod
    def get_current_time_str(fmt="%Y-%m-%d %H:%M:%S"):
        """
        获取当前时间字符串
        :param fmt: 时间格式
        :return: 格式化后的时间字符串
        """
        return datetime.now().strftime(fmt)

    @staticmethod
    def read_test_data(file_path):
        """
        从 Excel 文件中读取测试数据
        :param file_path: Excel 文件路径
        :return: 测试数据列表，每个元素为字典
        """
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        data = []
        headers = [cell.value for cell in sheet[1]]  # 获取表头
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data.append(dict(zip(headers, row)))
        return data

    @staticmethod
    def write_env_config(data, section='login', filename="data/env.ini"):
        config = configparser.ConfigParser()

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(project_root, filename)
        dir_name = os.path.dirname(full_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        if os.path.exists(full_path):
            config.read(full_path, encoding='utf-8')  # ✅ 加上 encoding

        if not config.has_section(section):
            config.add_section(section)

        for key, value in data.items():
            config.set(section, key, str(value))

        with open(full_path, 'w', encoding='utf-8') as f:  # ✅ 使用 utf-8 写入
            config.write(f)

        print(f"已将 data 数据写入配置文件 {full_path}")


    @staticmethod
    def read_env_config(key, section='login', filename="data/env.ini"):
        """
        从 env.ini 中读取指定 section 下的配置项
        :param key: 要读取的键名
        :param section: 配置节名，默认为 'login'
        :param filename: 配置文件路径
        :return: 键值（字符串）或 None
        """
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(project_root, filename)

        config = configparser.ConfigParser()
        config.read(full_path, encoding='utf-8')  # ✅ 显式指定编码为 utf-8

        if config.has_section(section) and config.has_option(section, key):
            return config.get(section, key)
        else:
            return None

    @staticmethod
    def generate_realistic_industry_requirement():
        """
        生成一个真实的行业需求描述，格式为：
        \"{数量}{单位} {需求描述}\"，例如：
        - \"50人 会议接待\"
        - \"200件 周边定制\"
        - \"30套 宿舍空调安装\"
        """
        # 可选单位和数量范围
        units = ["人", "件", "台", "个", "套", "间"]
        quantity = random.randint(1, 300)
        unit = random.choice(units)

        # 真实行业需求模板
        realistic_requirements = [
            "会议接待", "周边定制", "宿舍空调安装", "场地搭建",
            "设备租赁", "系统部署", "技术咨询", "广告投放",
            "人员派遣", "物资运输", "仓储管理"
        ]

        requirement = random.choice(realistic_requirements)

        return f"{quantity}{unit} {requirement}"