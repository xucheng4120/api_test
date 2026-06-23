# testcases/test_posts_v2.py
# fixture 注入版用例，更简洁，复用性更好
# 通过 conftest.py 定义的 fixture 注入 api 客户端和测试数据，测试用例只关注测试逻辑，前后置统一管理，代码更清晰

import allure
from api.base_api import BaseApi

@allure.feature("文章管理")
class TestPostsV2:

    @allure.title("获取单篇文章 - 验证返回内容正确")
    @allure.description("请求 /posts/1，验证状态码200，id字段正确，title字段存在")
    @allure.severity("critical")
    @allure.story("查询文章")
    def test_get_post_success(self, api):
        with allure.step("发送 GET /posts/1 请求"):
            response = api.get("/posts/1")

        with allure.step("验证状态码为 200"):
            assert response.status_code == 200

        with allure.step("验证响应体字段正确"):
            body = response.json()
            assert body["id"] == 1
            assert "title" in body
            allure.attach(str(body), name="响应数据", attachment_type=allure.attachment_type.TEXT)

    @allure.title("获取所有文章 - 验证返回100条")
    @allure.description("请求 /posts，验证状态码200，数据条数为100")
    @allure.severity("normal")
    @allure.story("查询文章")
    def test_get_all_posts(self, api):
        with allure.step("发送 GET /posts 请求"):
            response = api.get("/posts")

        with allure.step("验证状态码为 200"):
            assert response.status_code == 200

        with allure.step("验证返回数据条数为 100"):
            assert len(response.json()) == 100
            allure.attach(f"共返回 {len(response.json())} 条", name="数据条数", attachment_type=allure.attachment_type.TEXT)

    @allure.title("创建文章 - 验证创建成功")
    @allure.description("POST /posts 创建一篇文章，验证状态码201，标题字段与入参一致")
    @allure.severity("critical")
    @allure.story("创建文章")
    def test_create_post(self, api, post_data):
        with allure.step("准备请求数据"):
            allure.attach(str(post_data), name="请求数据", attachment_type=allure.attachment_type.TEXT)

        with allure.step("发送 POST /posts 请求"):
            response = api.post("/posts", data=post_data)

        with allure.step("验证状态码为 201"):
            assert response.status_code == 201

        with allure.step("验证响应 title 与入参一致"):
            assert response.json()["title"] == post_data["title"]
            allure.attach(str(response.json()), name="响应数据", attachment_type=allure.attachment_type.TEXT)

    @allure.title("获取不存在的文章 - 验证返回404")
    @allure.description("请求一个不存在的文章 id=9999，验证接口正确返回404")
    @allure.severity("normal")
    @allure.story("异常场景")
    def test_get_nonexistent_post(self, api):
        with allure.step("发送 GET /posts/9999 请求"):
            response = api.get("/posts/9999")

        with allure.step("验证状态码为 404"):
            assert response.status_code == 404
            allure.attach(str(response.json()), name="响应数据", attachment_type=allure.attachment_type.TEXT)
            