# conftest.py
# pytest 的全局配置文件，定义公共的 fixture 和测试环境准备/清理逻辑,session/function 级别 fixture，前后置统一管理
# pytest_runtest_makereport hook 实现失败用例自动附加日志到 Allure 报告，提升调试效率
# 通过命令行参数 --env 选择测试环境，fixture 根据环境初始化 API 客户端，测试用例通过 fixture 注入使用，代码更简洁，复用性更好

import pytest
import allure
from api.base_api import BaseApi
from utils.logger import get_logger

logger = get_logger()


def pytest_addoption(parser):
    """注册命令行参数 --env"""
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="运行环境: test / staging / prod"
    )


@pytest.fixture(scope="session")
def env(request):
    """获取当前环境名"""
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def api(env):
    """根据环境初始化 API 客户端"""
    logger.info("=" * 50)
    logger.info(f"测试会话开始，当前环境: {env.upper()}")
    logger.info("=" * 50)

    api_client = BaseApi(env=env)

    yield api_client

    logger.info("=" * 50)
    logger.info("测试会话结束")
    logger.info("=" * 50)
    api_client.session.close()


@pytest.fixture(scope="function")
def post_data():
    return {
        "title": "自动化测试文章",
        "body": "这是测试内容",
        "userId": 1
    }


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """用例失败时，自动把日志附加到 Allure 报告"""
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
            allure.attach(
                last_lines,
                name="失败时的请求日志",
                attachment_type=allure.attachment_type.TEXT
            )

@pytest.fixture(scope="session")
def created_post_id(api):
    """
    依赖 api fixture，先创建一篇文章，
    返回 id 给后续用例使用，session 级别只创建一次
    """
    data = {"title": "共享文章", "body": "内容", "userId": 1}
    response = api.post("/posts", data=data)
    post_id = response.json()["id"]
    logger.info(f"前置：创建了文章，id={post_id}")

    yield post_id

    logger.info(f"后置：文章 id={post_id} 测试完毕")