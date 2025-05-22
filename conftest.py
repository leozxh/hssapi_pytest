import logging
import time
import pytest
import allure
from config.config import DOMAINS, ENV, DATA_PATH
from common.common_utils import CommonUtils


@pytest.fixture(scope="class")
def setup_test_data():
    """Fixture：为整个测试类加载测试数据"""
    file_path = DATA_PATH['test_cases']
    test_cases = CommonUtils.read_test_data(file_path)
    base_url = DOMAINS[ENV]
    return {
        'test_cases': test_cases,
        'base_url': base_url
    }


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("test_execution.log", encoding='utf-8'),  # 输出到文件
            logging.StreamHandler()  # 同时输出到控制台
        ]
    )

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_class():
    setup_logging()  # 设置日志
    logger = logging.getLogger(__name__)
    logger.info("===== 测试类开始执行 =====")

    file_path = DATA_PATH['test_cases']
    logger.info("已加载测试数据，路径：%s", file_path)

    yield

    logger.info("===== 测试类执行完成 =====")


@pytest.fixture(autouse=True)
def setup_and_teardown_method():
    """每个测试方法执行前后的初始化和清理"""
    logger = logging.getLogger(__name__)
    start_time = time.time()
    logger.info("Start testing")

    yield

    end_time = time.time()
    logger.info("End testing, 耗时 %.3f 秒", end_time - start_time)

@pytest.fixture(autouse=True)
def capture_logs_for_allure(caplog):
    caplog.set_level(logging.INFO)
    yield
    for record in caplog.records:
        if record.levelno >= logging.INFO:  # 只附加 INFO 及以上级别的日志
            allure.attach(
                record.getMessage(),
                name=f"日志信息 - {record.levelname}",
                attachment_type=allure.attachment_type.TEXT
            )

# 新增：确保直接运行测试文件时也能看到日志输出
if __name__ == "__main__":
    setup_logging()