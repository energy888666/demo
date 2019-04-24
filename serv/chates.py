# 作者：xiaozhang
# 日期：2019.03.21 上午 8:32
# 工具：PyCharm Python版本：3.6
from flask import Blueprint, request, jsonify, session, render_template, redirect
from settings import DB
import json
import os
chates = Blueprint("chates", __name__)

#单聊
@chates.route('/onetalk')
def onetalk():
    print(session.get("user")) #送session中获取用户zy
    user=session.get("user")
    user_info_list=list(DB.user.find({}))
    user_list=[]
    for i in user_info_list:
        user_list.append(i.get("name"))
    print(user_list) #当前的用户列表
    return render_template("onetalk.html",user=user,user_list=json.dumps(user_list))
