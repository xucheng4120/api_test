# -*- coding: utf-8 -*-
# testcases/test_student.py
# 测试学生相关接口的测试用例
# 包含：分页查询学生列表等

import pytest
import allure
from utils.data_loader import load_yaml

student_page_data = load_yaml("users.yaml")["student_page"]


@allure.feature("学生管理")
class TestStudent:

    @allure.title("分页查询学生列表 - 数据驱动")
    @allure.description("POST /csm/student/page，验证状态码、业务码、分页数据结构完整性")
    @allure.severity("critical")
    @allure.story("学生查询")
    @pytest.mark.parametrize(
        "case_data",
        student_page_data,
        ids=[item["case"] for item in student_page_data]
    )
    def test_student_page(self, api, case_data):
        with allure.step("准备请求数据"):
            allure.attach(str(case_data["data"]), name="请求参数",
                         attachment_type=allure.attachment_type.TEXT)

        with allure.step("发送 POST /csm/student/page 请求"):
            response = api.post("/csm/student/page", data=case_data["data"])

        with allure.step("验证 HTTP 状态码为 200"):
            assert response.status_code == 200

        with allure.step("验证业务码为 0，操作成功"):
            result = response.json()
            assert result["code"] == 0, f"业务失败：{result.get('msg')}"
            assert result["msg"] == "查询学生成功"

        with allure.step("验证分页数据结构完整"):
            data = result["data"]
            assert "records" in data, "缺少 records 字段"
            assert "total" in data,   "缺少 total 字段"
            assert "size" in data,    "缺少 size 字段"
            assert "current" in data, "缺少 current 字段"
            assert "pages" in data,   "缺少 pages 字段"

        with allure.step("验证分页参数与入参一致"):
            assert data["current"] == case_data["data"]["pageNum"], \
                f"当前页码不符，期望{case_data['data']['pageNum']}，实际{data['current']}"
            assert data["size"] == case_data["data"]["pageSize"], \
                f"每页条数不符，期望{case_data['data']['pageSize']}，实际{data['size']}"

        with allure.step("验证 records 列表不为空"):
            assert len(data["records"]) > 0, "学生列表为空"
            assert len(data["records"]) <= case_data["data"]["pageSize"], \
                "返回条数超过 pageSize"

        with allure.step("验证每条记录的关键字段完整"):
            for student in data["records"]:
                assert "id" in student,    f"学生记录缺少 id 字段：{student}"
                assert "stuno" in student, f"学生记录缺少 stuno 字段：{student}"
                assert "sysUser" in student, f"学生记录缺少 sysUser 字段：{student}"
                assert "sysOrg" in student,  f"学生记录缺少 sysOrg 字段：{student}"
                assert student["sysUser"]["realName"], \
                    f"学生姓名为空：id={student['id']}"
                assert student["sysOrg"]["orgName"], \
                    f"班级名称为空：id={student['id']}"

        with allure.step("验证总数大于0"):
            assert data["total"] > 0, "学生总数为0"

        allure.attach(
            f"总学生数: {data['total']} | 总页数: {data['pages']} | 本页条数: {len(data['records'])}",
            name="分页统计",
            attachment_type=allure.attachment_type.TEXT
        )
        print(f"\n总学生数: {data['total']} | 总页数: {data['pages']} | 本页条数: {len(data['records'])}")