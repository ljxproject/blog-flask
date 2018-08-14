from app.extensions import db
from datetime import datetime

# 微博模型
class Post(db.Model):
    # 指定表名
    __tablename__ = 'posts'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # rid 用来表示该条推送是评论还是微博
    rid = db.Column(db.Integer, default=0)

    # 添加外键关系
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 其实还有个属性叫做user

