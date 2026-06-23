# testcases/test_posts.py
# 测试文章相关接口的测试用例
# 包含：获取文章列表、获取单篇文章、创建文章、删除文章等

from api.base_api import BaseApi

class TestPosts:
    
    def setup_method(self):
        """每个测试方法执行前初始化"""
        self.api = BaseApi()
    
    def test_get_post_success(self):
        """测试获取单篇文章 - 状态码200"""
        response = self.api.get("/posts/1")
        
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert "title" in response.json()
        print(f"\n响应数据：{response.json()}")
    
    def test_get_all_posts(self):
        """测试获取所有文章 - 返回100条"""
        response = self.api.get("/posts")
        
        assert response.status_code == 200
        assert len(response.json()) == 100
        print(f"\n共获取到 {len(response.json())} 条数据")
    
    def test_create_post(self):
        """测试创建文章"""
        data = {
            "title": "自动化测试文章",
            "body": "这是测试内容",
            "userId": 1
        }
        response = self.api.post("/posts", data=data)
        
        assert response.status_code == 201
        assert response.json()["title"] == "自动化测试文章"
        print(f"\n创建成功，返回id：{response.json()['id']}")
    
    def test_delete_post(self):
        """测试删除文章"""
        response = self.api.delete("/posts/1")
        
        assert response.status_code == 200
        print(f"\n删除成功，响应：{response.json()}")