# 作者：xiaozhang
# 日期：2019.03.19 下午 6:48
# 工具：PyCharm Python版本：3.6

from pymongo import MongoClient

#app的线上配置
class FlaskSetting(object):
    DEBUG=True
    SECRET_KEY="sdfasdfa112323!#4#@"
#  app的线下配置
class FlaskSettingTesting(object):
    TESTING = True
    SECRET_KEY = "xianxiakey"
    SESSION_COOKIE_NAME = "xianshangdeSession"

#数据库采用Mongodb进行存储,数据库的名称提前创建好,为AIwanju.
db_client=MongoClient(host="127.0.0.1",port=27017)
DB=db_client["Aikaoshi"]

## App数据传输协议
RET = {
    "code":0,
    "msg":"",
    "data":{}
}

