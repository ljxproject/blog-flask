from .users import User
from .posts import Post
from app.extensions import db

# 定义中间表
collections = db.Table('collections',
                       db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
                       )
