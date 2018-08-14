from flask import Blueprint, render_template, current_app, flash
from itsdangerous import TimedJSONWebSignatureSerializer as Serialzer
from app.extensions import db
from app.models import Post
from app.forms import PostForm
from flask_login import current_user
# 生成蓝本
main = Blueprint('main', __name__)


@main.route('/index/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    # 判断是否合法
    if form.validate_on_submit():
        user = current_user._get_current_object()
        # 如果合法则取出数据，保存
        post = Post(content=form.content.data, user=user)
        db.session.add(post)
        # 清空form中的数据
        form.content.data = ''
        # 提示用户
        flash('发布成功')
    # 返回
    # posts = Post.query.filter_by(rid=0)
    pagination = Post.query.filter_by(rid=0).order_by(Post.timestamp.desc()).paginate(per_page=3, max_per_page=8, error_out=False)
    posts = pagination.items
    return render_template('common/index.html', form=form, posts=posts, pagination=pagination)


# 第一个视图函数
@main.route('/token/')
def token():
    s = Serialzer(current_app.config['SECRET_KEY'])
    token = s.dumps({'id': None})
    return token
    # return render_template('common/index.html')

@main.route('/get_token/')
def get_token():
    s = Serialzer(current_app.config['SECRET_KEY'])
    token = s.loads('eyJhbGciOiJIUzI1NiIsImlhdCI6MTUxNzkwMDIwOCwiZXhwIjoxNTE3OTAzODA4fQ.eyJpZCI6bnVsbH0.3GINupIjyxKVFVRWC5bymCIn942sXSCAbsMEIUMIE8w')
    return str(token)