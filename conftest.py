# conftest.py
# 这是 pytest 的配置文件，用于定义全局 fixture 和钩子函数
# 定义了一个 session 级别的 fixture `api`，在测试会话开始时初始化 API 客户端并自动登录获取 token，测试用例通过参数注入使用这个 fixture，测试会话结束时关闭 session
# 还定义了一个 function 级别的 fixture `post_data`，用于提供测试数据，测试用例可以根据需要使用或覆盖这个 fixture
# 通过 pytest_runtest_makereport 钩子函数在测试失败时读取最新的日志文件内容，并将最后50行日志作为附件添加到 Allure 报告中，方便调试和问题定位

import pytest
import allure
from api.base_api import BaseApi
from utils.logger import get_logger

logger = get_logger()


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="test",
                     help="运行环境: test / staging / prod")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def api(env):
    """初始化 API 客户端，自动登录获取 token"""
    logger.info("=" * 50)
    logger.info(f"测试会话开始，当前环境: {env.upper()}")

    api_client = BaseApi(env=env)

    # 自动登录获取 token
    # 登录账号和密码可以根据不同环境配置在 config.py 中，或者从安全的地方获取
    login_accounts = {
        "test": {
            "username": "jan001",
            "password": "N3yRztIoMs6qK6SZRbUbGS/09apI0lXGVkAyjiMowcp9p2rX7owsnjDjWkzwuAGdScBiuRtk+wtV8IeRAun7Fxv5EEHodA7S+6tiKl9FmSrEIEod+h+tvwOrtz3HIaqXJPSpG8MmR7xSmNXiElAN7307B8D11UAKPgfdX8jchLU="
        },
        "staging": {
            "username": "jan001",
            "password": "N3yRztIoMs6qK6SZRbUbGS/09apI0lXGVkAyjiMowcp9p2rX7owsnjDjWkzwuAGdScBiuRtk+wtV8IeRAun7Fxv5EEHodA7S+6tiKl9FmSrEIEod+h+tvwOrtz3HIaqXJPSpG8MmR7xSmNXiElAN7307B8D11UAKPgfdX8jchLU="
        },
        "prod": {
            "username": "jan001",
            "password": "N3yRztIoMs6qK6SZRbUbGS/09apI0lXGVkAyjiMowcp9p2rX7owsnjDjWkzwuAGdScBiuRtk+wtV8IeRAun7Fxv5EEHodA7S+6tiKl9FmSrEIEod+h+tvwOrtz3HIaqXJPSpG8MmR7xSmNXiElAN7307B8D11UAKPgfdX8jchLU="
        }
    }

    logger.info("正在登录...")
    response = api_client.post("/csm/gt", data=login_accounts[env])

    assert response.status_code == 200, f"登录请求失败：{response.text}"
    assert response.json()["code"] == 0, f"登录业务失败：{response.json()['msg']}"

    token = response.json()["data"]
    api_client.session.headers.update({
        "Authorization": f"Bearer {token}"
    })

    logger.info(f"登录成功，token 已注入")
    logger.info("=" * 50)

    yield api_client

    api_client.session.close()
    logger.info("测试会话结束")


@pytest.fixture(scope="function")
def post_data():
    return {}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        import os
        from datetime import datetime
        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")

        if os.path.exists(log_file):
            with open(log_file, encoding="utf-8") as f:
                lines = f.read().strip().splitlines()
            last_lines = "\n".join(lines[-50:])
            allure.attach(last_lines, name="失败时的请求日志",
                         attachment_type=allure.attachment_type.TEXT)