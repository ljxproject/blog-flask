from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,BooleanField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError
from app.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.extensions import  photos

# 定义注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', [Length(4,12, message='请输入4-12之间的字符')])
    password = PasswordField('密码', [Length(6,20, message='请输入6-20位之间的密码')])
    confirm = PasswordField('密码确认', [EqualTo('password', message='两次输入的密码不一致')])
    email = StringField('邮箱', [Email(message='请输入正确的邮箱地址')])
    submit = SubmitField('提交')

    # 自定义校验
    def validate_username(self, field):
        # 根据username 去数据库查找
        user = User.query.filter_by(username=field.data).first()
        # 判断user是否存在
        if user:
            # 抛出一个异常
            raise ValidationError('用户名已存在')

    # 做邮箱的校验
    def validate_email(self, field):
        # 根据email去数据库查找
        user = User.query.filter_by(email=field.data).first()
        # 判断user是否存在
        if user:
            # 抛出一个异常
            raise ValidationError('邮箱已存在')

# 登录form表单
class LoginForm(FlaskForm):
    username = StringField('用户名', [DataRequired(message='用户名不能为空')])
    password = PasswordField('密码', [DataRequired(message='密码不能为空')])
    # 添加记住我
    remember = BooleanField('记住我')
    submit = SubmitField('提交')


# 定义修改密码的form表单
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('原密码', [DataRequired(message='原密码不能为空')])
    new_password = PasswordField('新密码', [Length(6,20, message='请输入6-20位之间的密码')])
    confirm = PasswordField('密码确认', [EqualTo('new_password', message='两次输入的密码不一致')])
    submit = SubmitField('提交')

    # 自定义新老密码不能相等的校验
    def validate_new_password(self, field):
        # 取出新密码，和老密码对比。如果相等，则报错。
        if current_user.verify_password(field.data):
            raise ValidationError('新密码和原密码不能一致')


# 定义修改头像的form表单
class IconForm(FlaskForm):
    icon = FileField('头像', [FileRequired(message='请选择上传文件'),
                            FileAllowed(photos, message='请选择图片上传')])
    submit = SubmitField('提交')


# 定义找回密码的form表单
class ResetPassword(FlaskForm):
    email = StringField('邮箱', [Email(message='请输入正确的邮箱地址')])
    submit = SubmitField('提交')


# 定义重置密码的form表单
class ResetForm(FlaskForm):
    new_password = PasswordField('新密码', [Length(6,20, message='请输入6-20位之间的密码')])
    confirm = PasswordField('密码确认', [EqualTo('new_password', message='两次输入的密码不一致')])
    submit = SubmitField('提交')