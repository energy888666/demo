# 作者：xiaozhang
# 日期：2019.03.19 下午 6:46
# 工具：PyCharm Python版本：3.6

from flask import  Flask
from settings import FlaskSetting
from serv import user
from serv import chates

app =Flask(__name__)
#加载app的配置
app.config.from_object(FlaskSetting)
#蓝图注册
app.register_blueprint(user.user)
app.register_blueprint(chates.chates)

if __name__ == '__main__':
    app.run("0.0.0.0",9527)