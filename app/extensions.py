from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class


# 创建扩展对象
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
migrate = Migrate(db=db)
login_manager = LoginManager()
photos = UploadSet('photos', IMAGES)


# 初始化
def config_extensions(app):
    migrate.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # 初始化上传集
    configure_uploads(app, photos)

    # 配置文件上传大小
    patch_request_class(app, size=None)

    # login_manager的额外配置
    # 指定登录的视图函数
    login_manager.login_view = 'users.login'
    # 指定需要登录才能访问的提示信息
    login_manager.login_message = '需要登录后才能访问'
    # 设置session保护
    login_manager.session_protection = 'strong'