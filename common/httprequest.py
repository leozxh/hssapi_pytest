import requests

DEFAULT_HEADERS = {
    'Accept-Charset': 'utf-8',
    'Content-Type': 'application/json; charset=UTF-8'
}


class http_request:

    @staticmethod
    def http_get(url, params=None, headers=None):
        headers = headers or DEFAULT_HEADERS
        try:
            res = requests.get(url, params=params, headers=headers)
            res.raise_for_status()
            return res
        except requests.exceptions.RequestException as e:
            raise Exception(f"GET 请求失败: {e}")

    @staticmethod
    def http_post(url, data=None, json=None, headers=None, cookies=None):
        headers = headers or DEFAULT_HEADERS  # 默认使用 JSON 格式
        try:
            res = requests.post(url, data=data, json=json, headers=headers, cookies=cookies)
            res.raise_for_status()
            return res
        except requests.exceptions.RequestException as e:
            raise Exception(f"POST 请求失败: {e}")


    @staticmethod
    def build_auth_headers(access_token=None, x_encrypt_key=None, version=None):
        """
           构造认证请求头，支持可选 x-encrypt-key
           :param access_token: 登录 token
           :param x_encrypt_key: 加密密钥（如果 with_encrypt 为 True 必须提供）
           :param sys_source: SysSource 标识
           :param version: 客户端版本号
           :param with_encrypt: 是否包含 x-encrypt-key
           :return: headers 字典
           """
        headers = {
            'Content-Type': 'application/json'
        }
        if access_token:
            headers['Authorization'] = f'Bearer {access_token}'

        # 只有版本号大于等于 1.5.4 才添加 x_encrypt_key
        if version:
            headers['Version'] = version
            try:
                major, minor, patch = map(int, version.split('.'))
                if (major, minor, patch) >= (1, 5, 4):
                    if x_encrypt_key:
                        headers['X-Encrypt-Key'] = x_encrypt_key
            except ValueError:
                # 版本格式错误时也默认不加 x_encrypt_key
                pass

        return headers
