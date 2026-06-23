# testcases/test_users.py
# 测试用户相关接口的测试用例
# 包含：获取用户列表、获取单个用户、创建用户、更新用户、删除用户等

import pytest
import allure
from utils.data_loader import load_yaml

# 读取测试数据
create_data = load_yaml("users.yaml")["create_user"]
update_data = load_yaml("users.yaml")["update_user"]
patch_data = load_yaml("users.yaml")["patch_user"]


@allure.feature("用户管理")
class TestUsers:

    @allure.title("获取所有用户 - 验证返回10条")
    @allure.description("GET /users，验证状态码200，返回数据条数为10")
    @allure.severity("critical")
    @allure.story("查询用户")
    def test_get_user_list(self, api):
        with allure.step("发送 GET /users 请求"):
            response = api.get("/users")

        with allure.step("验证状态码为 200"):
            assert response.status_code == 200

        with allure.step("验证返回10条用户数据"):
            data = response.json()
            assert len(data) == 10
            allure.attach(f"共返回 {len(data)} 条", name="数据条数",
                         attachment_type=allure.attachment_type.TEXT)

    @allure.title("获取单个用户 - 验证返回内容正确")
    @allure.description("GET /users/1，验证状态码200，id和name字段正确")
    @allure.severity("critical")
    @allure.story("查询用户")
    def test_get_single_user(self, api):
        with allure.step("发送 GET /users/1 请求"):
            response = api.get("/users/1")

        with allure.step("验证状态码为 200"):
            assert response.status_code == 200

        with allure.step("验证响应字段正确"):
            data = response.json()
            assert data["id"] == 1
            assert data["name"] == "Leanne Graham"
            assert "email" in data
            allure.attach(str(data), name="响应数据",
                         attachment_type=allure.attachment_type.TEXT)

    @allure.title("获取不存在的用户 - 验证返回404")
    @allure.description("GET /users/999，验证接口正确返回404")
    @allure.severity("normal")
    @allure.story("异常场景")
    def test_get_not_found(self, api):
        with allure.step("发送 GET /users/999 请求"):
            response = api.get("/users/999")

        with allure.step("验证状态码为 404"):
            assert response.status_code == 404
            allure.attach(str(response.json()), name="响应数据",
                         attachment_type=allure.attachment_type.TEXT)

    @allure.title("创建用户 - 数据驱动")
    @allure.description("POST /users，参数化测试多组创建数据，验证状态码201和返回字段")
    @allure.severity("critical")
    @allure.story("创建用户")
    @pytest.mark.parametrize(
        "case_data",
        create_data,
        ids=[item["case"] for item in create_data]
    )
    def test_create_user(self, api, case_data):
        with allure.step("准备请求数据"):
            allure.attach(str(case_data["data"]), name="请求数据",
                         attachment_type=allure.attachment_type.TEXT)

        with allure.step("发送 POST /users 请求"):
            response = api.post("/users", data=case_data["data"])

        with allure.step("验证状态码为 201"):
            assert response.status_code == case_data["expected"]["status_code"]

        with allure.step("验证响应包含 name 字段"):
            result = response.json()
            assert result["name"] == case_data["data"]["name"]
            assert "id" in result
            allure.attach(str(result), name="响应数据",
                         attachment_type=allure.attachment_type.TEXT)

    @allure.title("完整更新用户 - 数据驱动")
    @allure.description("PUT /users/1，验证状态码200，返回更新后的数据")
    @allure.severity("normal")
    @allure.story("更新用户")
    @pytest.mark.parametrize(
        "case_data",
        update_data,
        ids=[item["case"] for item in update_data]
    )
    def test_update_user(self, api, case_data):
        with allure.step("准备请求数据"):
            allure.attach(str(case_data["data"]), name="请求数据",
                         attachment_type=allure.attachment_type.TEXT)

        with allure.step("发送 PUT /users/1 请求"):
            response = api.put("/users/1", data=case_data["data"])

        with allure.step("验证状态码为 200"):
            assert response.status_code == case_data["expected"]["status_code"]

        with allure.step("验证返回数据与入参一致"):
            result = response.json()
            assert result["name"] == case_data["data"]["name"]
            allure.attach(str(result), name="响应数据",
                         attachment_type=allure.attachment_type.TEXT)

    @allure.title("部分更新用户 - 只修改名字")
    @allure.description("PATCH /users/1，只传 name 字段，验证状态码200，名字更新成功")
    @allure.severity("normal")
    @allure.story("更新用户")
    @pytest.mark.parametrize(
        "case_data",
        patch_data,
        ids=[item["case"] for item in patch_data]
    )
    def test_patch_user(self, api, case_data):
        with allure.step("准备请求数据"):
            allure.attach(str(case_data["data"]), name="请求数据",
                         attachment_type=allure.attachment_type.TEXT)

        with allure.step("发送 PATCH /users/1 请求"):
            response = api.patch("/users/1", data=case_data["data"])

        with allure.step("验证状态码为 200"):
            assert response.status_code == case_data["expected"]["status_code"]

        with allure.step("验证名字已更新"):
            result = response.json()
            assert result["name"] == case_data["data"]["name"]
            allure.attach(str(result), name="响应数据",
                         attachment_type=allure.attachment_type.TEXT)

    @allure.title("删除用户 - 验证返回200")
    @allure.description("DELETE /users/1，验证状态码200")
    @allure.severity("normal")
    @allure.story("删除用户")
    def test_delete_user(self, api):
        with allure.step("发送 DELETE /users/1 请求"):
            response = api.delete("/users/1")

        with allure.step("验证状态码为 200"):
            assert response.status_code == 200
            allure.attach(str(response.json()), name="响应数据",
                         attachment_type=allure.attachment_type.TEXT)

    @allure.title("获取用户的文章列表")
    @allure.description("GET /users/1/posts，验证状态码200，返回数据不为空")
    @allure.severity("minor")
    @allure.story("查询用户")
    def test_get_user_posts(self, api):
        with allure.step("发送 GET /users/1/posts 请求"):
            response = api.get("/users/1/posts")

        with allure.step("验证状态码为 200"):
            assert response.status_code == 200

        with allure.step("验证返回数据不为空"):
            data = response.json()
            assert len(data) > 0
            allure.attach(f"共返回 {len(data)} 篇文章", name="文章数量",
                         attachment_type=allure.attachment_type.TEXT)