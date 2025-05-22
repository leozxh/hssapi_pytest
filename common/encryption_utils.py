import hmac
import hashlib
import time
import json
import base64
import os
from typing import Optional, Dict
from common.common_utils import CommonUtils
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class EncryptionUtils:
    @staticmethod
    def generate_nonce(length=24) -> str:
        """
        生成指定长度的随机字符串（用于防止重放攻击）
        :param length: 随机字符串长度，默认24位
        :return: 随机字符串
        """
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'  # 定义字符集，包含大小写字母和数字
        return ''.join(chars[int(random.random() * len(chars))] for _ in range(length))  # 随机选择字符生成指定长度的字符串

    @staticmethod
    def get_sign_payload(hmac_key: str, access_token: str, user_id: str, url_path: str) -> Dict[str, str]:
        """
        构造签名所需的基础参数对象
        :param hmac_key: HMAC 密钥
        :param access_token: 登录 token
        :param user_id: 用户 ID
        :param url_path: 接口路径
        :return: 包含签名信息的基础 payload
        """
        payload = {
            "token": access_token,  # 设置登录 token
            "userId": user_id,  # 设置用户 ID
            "timestamp": int(time.time()),  # 设置当前时间戳（秒级）
            "url": url_path,  # 设置接口路径
            "platform": "iOS",  # 设置平台信息
            "nonce": EncryptionUtils.generate_nonce()  # 生成随机 nonce 值
        }

        # 过滤并按key排序，移除 'sign' 键（如果存在）
        filtered_params = {
            k: v for k, v in sorted(payload.items()) if k != 'sign'
        }

        # 拼接 key=value&key=value 格式，并追加 key=HMAC_KEY
        sign_string = '&'.join([f"{k}={v}" for k, v in filtered_params.items()])  # 拼接参数为字符串
        sign_string += f"&key={hmac_key}"  # 添加 HMAC 密钥到签名字符串

        # 计算 HMAC-SHA256 签名
        signature = hmac.new(
            hmac_key.encode('utf-8'),  # 将 HMAC 密钥编码为字节
            sign_string.encode('utf-8'),  # 将签名字符串编码为字节
            hashlib.sha256  # 使用 SHA256 哈希算法
        ).hexdigest()  # 计算 HMAC 值并转换为十六进制字符串

        payload['sign'] = signature  # 将签名添加到 payload 中
        return payload  # 返回包含签名的 payload

    @staticmethod
    def aes_encrypt(plain_text: str, aes_key: str, iv: str) -> str:
        """
        使用 AES-CBC 模式加密文本
        :param plain_text: 明文字符串
        :param aes_key: AES 密钥
        :param iv: 初始化向量
        :return: Base64 编码的加密结果
        """
        key_bytes = aes_key.encode('utf-8')  # 将 AES 密钥编码为字节
        iv_bytes = iv.encode('utf-8')  # 将初始化向量编码为字节

        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)  # 创建 AES 加密器
        padded_data = pad(plain_text.encode('utf-8'), AES.block_size)  # 对明文进行填充
        encrypted = cipher.encrypt(padded_data)  # 加密填充后的数据

        return base64.b64encode(encrypted).decode('utf-8')  # 将加密结果编码为 Base64 字符串

    @classmethod
    def get_x_encrypt_key(cls, url_path: str) -> str:
        """
        获取用于请求头的 x-encrypt-key
        :param url_path: 接口路径
        :return: Base64 编码的加密结果
        """
        access_token = CommonUtils.read_env_config("accesstoken", section="login")  # 从环境变量中读取 access_token
        user_id = CommonUtils.read_env_config("userid", section="login")  # 从环境变量中读取 user_id
        hmac_key = CommonUtils.read_env_config("hmackey", section="aes")  # 从环境变量中读取 HMAC 密钥
        aes_key = CommonUtils.read_env_config("aeskey", section="aes")  # 从环境变量中读取 AES 密钥
        iv = CommonUtils.read_env_config("iv", section="aes")  # 从环境变量中读取初始化向量

        if not all([access_token, user_id, hmac_key, aes_key, iv]):  # 检查所有必要参数是否都已提供
            raise ValueError("缺少必要的加密参数，请检查环境变量配置")  # 如果有参数缺失，抛出异常

        # 构造 payload
        payload = {
            "token": access_token,  # 设置登录 token
            "userId": user_id,  # 设置用户 ID
            "timestamp": int(time.time() * 1000),  # 设置当前时间戳（毫秒级）
            "url": url_path,  # 设置接口路径
            "platform": "iOS",  # 设置平台信息
            "nonce": cls.generate_nonce()  # 生成随机 nonce 值
        }

        # 过滤并排序参数，移除 'sign' 键（如果存在）
        filtered_params = dict(sorted((k, v) for k, v in payload.items() if k != 'sign'))

        # 拼接签名字符串
        sign_string = "&".join([f"{k}={v}" for k, v in filtered_params.items()])  # 拼接参数为字符串
        sign_string += f"&key={hmac_key}"  # 添加 HMAC 密钥到签名字符串

        # 计算 HMAC-SHA256
        signature = hmac.new(hmac_key.encode('utf-8'), sign_string.encode('utf-8'), hashlib.sha256).hexdigest()  # 计算 HMAC 值

        payload['sign'] = signature  # 将签名添加到 payload 中

        # AES 加密
        encrypted_json = cls.aes_encrypt(json.dumps(payload), aes_key, iv)  # 将 payload 转换为 JSON 字符串并加密

        # # 打印调试信息
        # print("Sign String:", sign_string)  # 打印签名字符串
        # print("Signature:", signature)  # 打印签名结果
        # print("Payload:", json.dumps(payload))  # 打印完整的 payload
        # print("Encrypted Result:", encrypted_json)  # 打印加密结果

        return encrypted_json  # 返回加密结果