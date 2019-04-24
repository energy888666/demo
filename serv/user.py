# 作者：xiaozhang
# 日期：2019.03.19 下午 6:53
# 工具：PyCharm Python版本：3.6

from flask import Blueprint, request, jsonify, session, render_template, redirect
from settings import DB, RET
from wtforms import Form, validators, widgets
from wtforms.fields import core
from wtforms.fields import html5
from wtforms.fields import simple
import os
user = Blueprint("user", __name__)


class RegisterForm(Form):
    name = simple.StringField(
        label="用户名",
        validators=[
            validators.DataRequired(message="用户名不能为空")
        ],
        widget=widgets.TextInput(),
        render_kw={"class": "form-control"},
        default="zy"
    )
    pwd = simple.PasswordField(
        label="密码",
        validators=[
            validators.DataRequired(message="密码不能为空")
        ]
    )
    pwd_confim = simple.PasswordField(
        label="重复密码",
        validators=[
            validators.DataRequired(message='重复密码不能为空.'),
            validators.EqualTo('pwd', message="两次密码不一致")
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )

# 注册的功能
@user.route("/reg", methods=["POST", "GET"])
def reg():
    if request.method == "GET":
        form = RegisterForm()  # 一般这么写
        return render_template("reg.html", form=form)
    else:
        form = RegisterForm(formdata=request.form)
        if form.validate():  # 判断是否验证成功
            print(form.data)  # "用户提交的数据 {'name': 'zy', 'pwd': '123', 'pwd_confim': '123'}
            user_dic = form.data
            user_dic.pop("pwd_confim")  # 删除重复密码
            # 获取上传的文件
            # print(request.files)
            my_file = request.files["file"]
            # print(my_file.filename)
            # 将用户提交的图片保存在img文件夹下
            user_tx = os.path.join("img", my_file.filename)
            # print(user_tx)
            my_file.save(user_tx)  # 保存文件,里面可以写完整路径+文件名
            # print(user_dic)
            user_dic["avatar_name"] = my_file.filename
            # 数据库进行存储
            DB.user.insert_one(user_dic)
            return redirect('/login')
        else:
            print(form.errors)  # 所有的错误信息
            return render_template('reg.html', form=form)


class LoginForm(Form):
    '''Form'''
    name = simple.StringField(
        label="用户名",
        widget=widgets.TextInput(),
        validators=[
            validators.DataRequired(message="用户名不能为空"),
            validators.Length(max=8, min=1, message="用户名长度必须大于%(max)d且小于%(min)d")
        ],
        render_kw={"class": "form-control"}  # 设置属性 ,前端可以根据类名进行样式的定义
    )

    pwd = simple.PasswordField(
        label="密码",
        validators=[
            validators.DataRequired(message="密码不能为空"),
            validators.Length(max=8, min=1, message="密码长度必须大于%(max)d且小于%(min)d"),
            validators.Regexp(regex="\d+", message="密码必须是数字"),
        ],
        widget=widgets.PasswordInput(),
        render_kw={"class": "form-control"}
    )


# 登陆的功能
@user.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        form = LoginForm()
        return render_template("login.html", form=form)
    else:
        login_form_data = LoginForm(formdata=request.form)
        if login_form_data.validate():
            print(login_form_data.data)  # {'name': 'zy', 'pwd': '123'}
            res = DB.user.find_one(login_form_data.data, {"password": 0})
            if res:
                # 设置session
                session["user"] = login_form_data.data.get("name")
                return redirect("/onetalk")
            else:
                msg="用户名或者密码错误"
                return render_template("login.html",msg=msg,form=login_form_data)

        else:
            print(login_form_data.errors, "错误信息")
            return render_template("login.html", form=login_form_data)


