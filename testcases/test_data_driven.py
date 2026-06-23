# testcases/test_data_driven.py
# 数据驱动测试用例，从 yaml 文件读取多组测试数据，使用 pytest.mark.parametrize 参数化测试
# 通过 ids 参数为每组数据指定一个用例 id，运行时更清晰，方便定位问题，测试用例逻辑简单，专注于断言，数据和测试逻辑分离，维护更方便,YAML 数据驱动参数化

import pytest
from utils.data_loader import load_yaml

# 读取 yaml 数据
test_data = load_yaml("posts.yaml")["create_post"]

class TestDataDriven:

    @pytest.mark.parametrize(
        "case_data",
        test_data,
        ids=[item["case"] for item in test_data]  # 用 case 名作为用例 id
    )
    def test_create_post(self, api, case_data):
        """数据驱动：一个方法跑多组数据"""
        response = api.post("/posts", data=case_data["data"])
        
        assert response.status_code == case_data["expected"]["status_code"]
        print(f"\n【{case_data['case']}】passed，状态码={response.status_code}")