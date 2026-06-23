# config/config.py
# 统一管理环境配置
# 例如：基础 URL、请求头、超时时间等，方便维护和切换环境
# EnvConfig 类提供静态方法获取不同环境的配置，支持 test/staging/prod 环境，使用时通过 EnvConfig.get("test") 获取对应环境的配置字典

class EnvConfig:
    """各环境配置"""

    TEST = {
        "base_url": "https://jsonplaceholder.typicode.com",
        "timeout": 10,
        "headers": {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    }

    STAGING = {
        "base_url": "https://jsonplaceholder.typicode.com",  # 模拟预发环境
        "timeout": 15,
        "headers": {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Env": "staging"
        }
    }

    PROD = {
        "base_url": "https://jsonplaceholder.typicode.com",  # 模拟生产环境
        "timeout": 20,
        "headers": {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Env": "prod"
        }
    }

    @classmethod
    def get(cls, env):
        env_map = {
            "test": cls.TEST,
            "staging": cls.STAGING,
            "prod": cls.PROD
        }
        config = env_map.get(env)
        if not config:
            raise ValueError(f"不支持的环境: {env}，可选值: test / staging / prod")
        return config