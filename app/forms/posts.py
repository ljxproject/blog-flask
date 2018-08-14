from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Length


# 定义微博发布的表单
class PostForm(FlaskForm):
    content = TextAreaField('', render_kw={'style': 'height:100px','placeholder': '这一刻的想法...'}, validators=[Length(4,200,message='说话要注意分寸')])
    submit = SubmitField('发布', render_kw={'style': 'float:right'})



