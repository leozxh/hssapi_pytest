import pytest
from common.common_utils import CommonUtils
import subprocess
import os
import shutil


def run_tests():
    CommonUtils.add_project_root_to_path()

    # 新增：集中管理路径配置
    CONFIG = {
        "project_root": os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "test_dir": "testcases",
        "allure_output_dir": "allure_output",  # 主输出目录
        "allure_report_subdir": "data",     # 子目录：原始数据
        "allure_html_report_subdir": "html" # 子目录：HTML 报告
    }

    project_root = CONFIG["project_root"]
    test_dir = os.path.join(project_root, CONFIG["test_dir"])
    allure_output_dir = os.path.join(project_root, CONFIG["allure_output_dir"])
    allure_report_dir = os.path.join(allure_output_dir, CONFIG["allure_report_subdir"])
    allure_html_report_dir = os.path.join(allure_output_dir, CONFIG["allure_html_report_subdir"])

    # 清空旧的 allure 结果目录并创建新目录
    if os.path.exists(allure_output_dir):
        shutil.rmtree(allure_output_dir)
    os.makedirs(allure_report_dir)
    os.makedirs(allure_html_report_dir, exist_ok=True)

    # 执行测试并生成 Allure 结果
    pytest.main(["-v",
                 f"{test_dir}/hsslogin.py",
                 f"{test_dir}/smart_business_order.py",
                 "--alluredir", allure_report_dir])

    # 使用 Allure 的完整路径调用（请根据你的实际安装路径修改）
    allure_bat_path = r"D:\python310\Lib\site-packages\allure-2.34.0\allure-2.34.0\bin\allure.bat"
    subprocess.run([
        allure_bat_path, "generate",
        allure_report_dir,
        "-o", allure_html_report_dir,
        "--clean"
    ], encoding='utf-8')



if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"[ERROR] 测试运行失败: {e}")