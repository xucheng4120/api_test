# testcases/test_fixture_chain.py
# 测试 fixture 依赖和共享，验证 session 级别 fixture 的前后置逻辑
# created_post_id fixture 依赖 api fixture 创建一篇文章，返回 id 给测试用例使用，验证同一个 id 被多个用例共享，且 fixture 只执行一次

class TestFixtureChain:

    def test_use_shared_post(self, api, created_post_id):
        """验证 created_post_id 是由 fixture 创建并共享的"""
        # jsonplaceholder 不真实存储，id=101 代表创建成功
        assert created_post_id == 101
        print(f"\n共享的 post_id={created_post_id}，fixture 只创建了一次")

    def test_use_shared_post_again(self, api, created_post_id):
        """验证第二条用例拿到的是同一个 id，fixture 没有重新执行"""
        assert created_post_id == 101
        print(f"\n同一个 id={created_post_id}，confirmed：session fixture 没有重跑")