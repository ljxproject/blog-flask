from app.config import config
from flask import Flask, render_template
from app.extensions import config_extensions
from .views import config_blueprint


# 自定义错误页面
def config_errorhandler(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html')


# 封装创建app的函数
def create_app(config_name):
    # 创建flask实例对象
    app = Flask(__name__)
    # 初始化
    app.config.from_object(config.get(config_name, 'default'))
    # 执行额外的初始化操作
    config[config_name].init_app(app)
    # 导入扩展
    config_extensions(app)
    # 注册蓝本
    config_blueprint(app)
    # 调用自定义错误处理函数
    config_errorhandler(app)
    # 返回生成的app
    return app




