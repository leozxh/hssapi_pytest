import logging
from common.httprequest import http_request
from common.common_utils import CommonUtils
from config.config import DOMAINS, ENV, DATA_PATH

logger = logging.getLogger(__name__)

class TestGetAESKey:

    def test_get_aes_key(self):
        """获取AES密钥"""
        base_url = DOMAINS[ENV]
        file_path = DATA_PATH['test_cases']
        test_cases = CommonUtils.read_test_data(file_path)
        aes_case = test_cases[1]
        aeskey_path = aes_case['Path']
        aes_key_url = f"{base_url}{aeskey_path}"

        logger.info("====== 开始获取AES密钥 ======")
        logger.info(f"请求URL: {aes_key_url}")

        try:
            response = http_request.http_get(aes_key_url)
            logger.info("响应状态码: %d", response.status_code)
            logger.info("响应内容: %s", response.text)

            assert response.status_code == 200, "获取AES密钥失败"
            response_data = response.json().get('data', {})
            CommonUtils.write_env_config(response_data, section='aes', filename="data/env.ini")
            logger.info("AES密钥已成功写入配置文件")

        except Exception as e:
            logger.error("获取AES密钥失败")
            logger.error("响应状态码: %d", response.status_code)
            logger.error("响应内容: %s", response.text)
            raise e

        finally:
            logger.info("====== 获取AES密钥结束 ======")