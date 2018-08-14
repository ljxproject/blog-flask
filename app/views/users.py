from flask import Blueprint, render_template, flash, current_app, redirect, url_for, request, jsonify
from app.forms import RegisterForm, LoginForm, ChangePasswordForm, IconForm, ResetPassword, ResetForm
from app.models import User
from app.extensions import db
from app.email import send_mail
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import photos
import os
from PIL import Image
# 生成蓝本
users = Blueprint('users', __name__)


# 第一个视图函数
@users.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # 判断提交的数据是否合法
    if form.validate_on_submit():
        # 如果 合法则保存用户对象
        # 先创建user对象
        user = User(
            username=form.username.data,
            password=form.password.data,
            email = form.email.data
        )
        db.session.add(user)
        db.session.commit()
        # 生成token
        token = user.generate_activate_token()
        # 然后发送激活邮件
        send_mail(form.email.data, '激活邮件', 'email/activate',
                  username=form.username.data,
                  token=token)
        # 提示用户邮件已发送，去激活。
        flash('激活邮件已发送，请进入激活邮件点击链接进行激活。')
        # 返回首页
        return redirect(url_for('main.index'))
    return render_template('users/register.html', form=form)


@users.route('/activate/<token>/')
def activate(token):
    is_active , u = User.check_activate_token(token)
    # 判断是否激活
    if is_active:
        flash('激活成功！')
        return redirect(url_for('main.index'))
    else:
        flash('激活失败，请重新注册！')
        return redirect(url_for('users.register'))


# 登录视图
@users.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # 判断数据是否合法
    if form.validate_on_submit():
        # 如果合法则根据用户名查找对象
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            # 查不到则提示用户名错误
            flash('用户名或密码错误')
        # 如果能查到则校验密码是否相等
        elif user.verify_password(form.password.data):
            # 密码校验成功，则登录
            login_user(user, remember=form.remember.data)
            flash('登录成功')
            # 回到首页
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('用户名或密码错误')
    return render_template('users/login.html', form=form)


# 注销
@users.route('/logout/')
def logout():
    logout_user()
    flash('注销成功')
    return redirect(url_for('main.index'))


# 测试登录才能访问
@users.route('/test/')
@login_required
def test():
    return '登录测试访问！'


# 显示个人详情
@users.route('/profile/')
def profile():
    return render_template('users/profile.html')


# 修改密码
@users.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    # 首先判断数据是否合法
    if form.validate_on_submit():
        # 获取真实的用户
        user = current_user._get_current_object()
        # 取出老密码，进行判断老密码是否正确。
        if user.verify_password(form.old_password.data):
            # 取出新密码，设置为新密码，保存。
            user.password = form.new_password.data
            db.session.add(user)
            # 提示用户密码修改成功
            flash('密码修改成功，请重新登录')
            # 退出并返回登录界面重新登录
            logout_user()
            return redirect(url_for('users.login'))
    return render_template('users/change_password.html', form=form)

# 生成随机字符串
def random_str(length=32):
    import random
    import string
    base_str = string.ascii_lowercase + string.digits
    return ''.join(random.choice(base_str) for _ in range(length))


# 修改头像
@users.route('/icon/', methods=['GET', 'POST'])
def icon():
    form = IconForm()
    # 取出真实对象
    user = current_user._get_current_object()
    # 判断数据是否合法
    if form.validate_on_submit():

        # 保存头像文件
        # 或取后缀
        suffix = os.path.splitext(form.icon.data.filename)[1]
        # 生成随机文件名
        filename = random_str() + suffix
        # 使用上传集的保存方法即可保存
        photos.save(form.icon.data, name=filename)
        # 生成文件名的绝对路径
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
        # 生成缩略图
        image = Image.open(pathname)
        # 修改图片大小
        image.thumbnail((128, 128))
        # 保存修改后的文件
        image.save(pathname)

        # 先判断是否是default，如果是default就别删了。
        if user.icon != 'default.jpg':
            # 删除原头像
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], user.icon))
        # 取出数据，赋值给user的icon属性
        user.icon = filename
        # 保存数据
        db.session.add(user)
        # 提示用户修改成功
        flash('头像修改成功')

    # 返回图片的url路径
    img_url = photos.url(user.icon)
    return render_template('users/icon.html', form=form, img_url=img_url)


# 定义忘记密码函数
@users.route('/forget_password/', methods=['GET', 'POST'])
def forget_password():
    form = ResetPassword()
    # 首先判断数据是否合法。
    if form.validate_on_submit():
        # 取出邮箱，判断是否存在这个邮箱的用户
        user = User.query.filter_by(email=form.email.data).first()
        # 存在则发送邮件，不存在也不提示。
        token = user.generate_activate_token()
        if user:
            send_mail(form.email.data, '重置密码', 'email/reset_password', username=user.username, token=token)
            return render_template('users/reset_password_done.html')
            # 返回邮件已发送的页面
    return render_template('users/reset_password.html', form=form)


@users.route('/reset_password/<token>/', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetForm()
    # 判断数据是否合法
    if form.validate_on_submit():
        # 从token中取出用户
        # 判断token是否正确,并解析token
        is_active, u = User.check_activate_token(token)
        if is_active:
        # 取出数据，赋值给password，保存
            u.password = form.new_password.data
            db.session.add(u)
            # 提示，并返回。
            flash('重置密码成功，请登录')
            return redirect(url_for('users.login'))
    return render_template('users/reset_password_form.html', form=form)


# 定义用户收藏微博的视图函数
@users.route('/collect/<int:pid>/')
def collect(pid):
    # 判断用户是否收藏，如果收藏了，就取消收藏，没收藏，就收藏
    if current_user.is_favorite(pid):
        # 取消收藏
        current_user.cancel_favorite(pid)
    else:
        current_user.add_favorite(pid)
    return jsonify({'result': 'ok'})