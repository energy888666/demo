from geventwebsocket.server import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket
from  flask import Flask,request,render_template
import json
from  settings import DB
app=Flask(__name__)
# user_socket_dict = {"客户端1":<geventwebsocket.websocket.WebSocket object at 0x000002699374A730>,
# "客户端2":<geventwebsocket.websocket.WebSocket object at 0x000002699374A5F8>}

user_socket_dict={}
@app.route("/ws/<nickname>") #接受用户的名字
def my_ws_func(nickname):
    print(nickname)
    user_socket=request.environ.get("wsgi.websocket")#type:WebSocket
    user_socket_dict[nickname]=user_socket
    print(len(user_socket_dict),user_socket_dict)
    while 1:
        msg=user_socket.receive()#接收客户端发送来的消息
        msg=json.loads(msg)
        #构造msg数据结构如下:
        '''
        {
         to_user:客户端1,
         from_user:客户端2,
         msg:发送的内容   
        }
        '''
        print(msg)
        #进行消息的存储
        # DB.chats.inset
        to_user_socket=user_socket_dict.get(msg.get("to_user"))  #获取客户端1的websocket
        msg_json=json.dumps(msg)
        to_user_socket.send(msg_json) #发送给客户端1

# @app.route('/onetalk')
# def one_p():
#     return render_template("onetalk.html")

if __name__ == '__main__':
    http_serve=WSGIServer(("0.0.0.0",9002),application=app,handler_class=WebSocketHandler)
    http_serve.serve_forever()