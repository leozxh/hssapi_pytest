import allure
from common.httprequest import http_request
from config.config import DOMAINS, ENV, DATA_PATH
from common.common_utils import CommonUtils
import logging

logger = logging.getLogger(__name__)

class TestLogin:
    @allure.title("用户登录测试 - 成功场景")
    def test_001_login_newaccount(self):
        self._testMethodDoc = '登录操作'
        base_url = DOMAINS[ENV]
        file_path = DATA_PATH['test_cases']
        test_cases = CommonUtils.read_test_data(file_path)

        # 直接获取第一条用例（索引为 0）
        case = test_cases[0]

        login_path = case['Path']
        login_url = f"{base_url}{login_path}"

        login_data = {
            'userName': case['userName'],
            'password': case['password'],
            'loginType': case['loginType'],
        }

        login_msg = http_request.http_post(login_url, json=login_data)

        # 打印请求信息（可选）
        logger.info("====== 请求信息 ======")
        logger.info(f"请求 URL:{login_path}")
        logger.info(f"请求方法: POST")
        logger.info("======================")

        try:
            assert case['ExpectedResult'] == login_msg.json()['msg']  # 使用 pytest 原生断言
            logger.info(f"{case['CaseID']} 测试通过")

            response_data = login_msg.json().get('data', {})  # 获取响应中的 data 部分
            filtered_data = {  # 过滤需要的数据
                'userid': response_data.get('userId'),  # 用户 ID
                'accesstoken': response_data.get('accessToken'),  # 访问令牌
                'roles': response_data.get('roles')  # 角色信息
            }
            CommonUtils.write_env_config(filtered_data, filename="data/env.ini")  # 将过滤后的数据写入环境变量文件

        except Exception as e:  # 捕获异常
            logger.error(f"{case['CaseID']} 测试不通过")  # 打印测试失败信息
            logger.error("响应状态码: %d", login_msg.status_code)  # 打印响应状态码
            logger.error("响应内容: %s", login_msg.text)  # 打印响应内容
            raise e  # 抛出异常