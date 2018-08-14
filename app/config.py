import os

# 获取根目录
base_dir = os.path.abspath(os.path.dirname(__file__))


# 通用配置
class Config:
    # 秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'

    # 数据库配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 邮件配置
    MAIL_SERVER = 'smtp.1000phone.com'
    MAIL_USERNAME = 'xuke@1000phone.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '123456'

    # 配置上传文件目录
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'static/upload')
    # 配置上传文件的大小
    MAX_CONTENT_LENGTH = 1024 * 1024 * 10
    # 额外的初始化
    @staticmethod
    def init_app(app):
        pass


# 开发环境
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'weibo-dev.sqlite')


# 测试环境
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'weibo_test.sqlite')


# 生产环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'weibo.sqlite')


# 定义一个字典。
config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}