from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, flash
from itsdangerous import BadSignature, SignatureExpired
from flask_login import UserMixin
from .posts import Post


# 定义User模型
class User(UserMixin, db.Model):
    # 表名
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(256))
    email = db.Column(db.String(64), unique=True)
    confirmed = db.Column(db.Boolean, default=False)

    # 添加头像字段
    icon = db.Column(db.String(64), default='default.jpg')

    # 添加关系
    posts = db.relationship('Post', backref='user', lazy='dynamic')


    # 添加多对多关系，表示收藏微博
    favorites = db.relationship('Post', secondary='collections',
                                backref=db.backref('users', lazy='dynamic'),
                                lazy='dynamic')

    # 判断是否收藏某个微博
    def is_favorite(self, pid):
        # 获取所有该用户收藏的微博
        favorites = self.favorites.all()
        posts = list(filter(lambda p: p.id == pid, favorites))
        if len(posts) > 0:
            return True
        return False

    # 添加收藏
    def add_favorite(self, pid):
        # 先获取pid对应的微博
        post = Post.query.get(pid)
        # 将其加入favorites
        self.favorites.append(post)

    # 取消收藏
    def cancel_favorite(self, pid):
        post = Post.query.get(pid)
        self.favorites.remove(post)


    def __repr__(self):
        return self.username

    # 密码不能直接访问 。比如不能user.password，如果直接访问，则报个错
    @property
    def password(self):
        raise AttributeError('密码不能直接访问')

    # 设置密码，就是把user.password = form.password.data操作转化成
    # user.password_hash = hash(form.password.data)
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 生成激活token
    def generate_activate_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        # 生成token
        return s.dumps({'id': self.id})

    # 检查密码是否正确
    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)

    # 检查激活token是否正确
    @staticmethod
    def check_activate_token(token):
        # 生成serializer对象
        s = Serializer(current_app.config['SECRET_KEY'])
        # 对解析token进行异常处理
        try:
            data = s.loads(token)
        except BadSignature:
            flash('无效的token！')
            return False
        except SignatureExpired:
            flash('token已过期')
            return False
        # 从data中获取数据，即user.id
        # 根据获取到的user.id去查找用户
        id = data.get('id')
        user = User.query.get(id)
        # 判断用户是否存在
        if not user:
            flash('用户不存在，请重新注册')
            return False
        # 判断用户是否激活，只有没激活的才需要激活
        if not user.confirmed:
            # 设置为激活
            user.confirmed = True
            db.session.add(user)
        return True, user


from app.extensions import login_manager


# 设置flask_login的回调函数，即：flask_login获取user对象的方法
@login_manager.user_loader
def load_user(uid):
    user = User.query.get(int(uid))
    return user