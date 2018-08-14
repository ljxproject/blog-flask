from .extensions import mail
from flask import current_app, render_template
from flask_mail import Message
from threading import Thread


def async_send_mail(app, msg):
    # 打开app的上下文，用来发送邮件。因为发送邮件需要使用app的上下文。
    with app.app_context():
        mail.send(msg)


# 将发送邮件的代码封装成一个函数，方便重复使用
def send_mail(to, subject, template, **kwargs):
    # 通过代理对象找到app实例对象
    app = current_app._get_current_object()

    msg = Message(subject=subject,
                  recipients=[to],
                  sender=app.config['MAIL_USERNAME'])
    msg.html = render_template(template+'.html', **kwargs)
    msg.body = render_template(template+'.txt', **kwargs)

    # 新建一个线程，用来发送邮件。
    thr = Thread(target=async_send_mail, args=[app, msg])
    # 启动线程
    thr.start()
    return thr