# api/base_api.py
# 封装 GET/POST/PUT/DELETE 请求基类
# 统一管理请求细节，如 base_url、headers、timeout 等，提供简洁的接口供测试用例调用
# 内部实现请求日志记录，方便调试和问题定位，使用 requests.Session 复用连接，提高性能，支持 JSON 请求体自动转换，简化测试用例代码
# 通过 EnvConfig 获取环境配置，支持多环境切换，适应不同测试需求，日志记录请求和响应详情，提升可观察性和调试效率

import time
import requests
from config.config import EnvConfig
from utils.logger import get_logger

logger = get_logger()


class BaseApi:

    def __init__(self, env="test"):
        config = EnvConfig.get(env)
        self.base_url = config["base_url"]
        self.timeout = config["timeout"]
        self.session = requests.Session()
        self.session.headers.update(config["headers"])
        logger.info(f"API 客户端初始化完成 | 环境: {env} | BaseURL: {self.base_url}")

    def _log_request(self, method, url, **kwargs):
        logger.info(f"┌─ 请求开始 {'─' * 40}")
        logger.info(f"│  {method.upper()} {url}")
        if kwargs.get("params"):
            logger.info(f"│  Params: {kwargs['params']}")
        if kwargs.get("json"):
            logger.info(f"│  Body:   {kwargs['json']}")

    def _log_response(self, response, elapsed):
        status = response.status_code
        level = logger.info if status < 400 else logger.error
        level(f"│  Status: {status} | 耗时: {elapsed:.3f}s")
        try:
            level(f"│  Response: {response.json()}")
        except Exception:
            level(f"│  Response: {response.text[:200]}")
        logger.info(f"└─{'─' * 44}")

    def _request(self, method, path, **kwargs):
        url = self.base_url + path
        self._log_request(method, url, **kwargs)
        start = time.time()
        response = self.session.request(
            method, url, timeout=self.timeout, **kwargs
        )
        elapsed = time.time() - start
        self._log_response(response, elapsed)
        return response

    def get(self, path, params=None):
        return self._request("GET", path, params=params)

    def post(self, path, data=None):
        return self._request("POST", path, json=data)

    def put(self, path, data=None):
        return self._request("PUT", path, json=data)

    def delete(self, path):
        return self._request("DELETE", path)
    
    def patch(self, path, data=None):
        return self._request("PATCH", path, json=data)