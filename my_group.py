from geventwebsocket.server import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket
from flask import Flask, request, render_template

app = Flask(__name__)
#群聊,需要创建一个列表,这样每个人的信息大家都能看到
user_socket_lst=[]
@app.route('/ws')
def my_ws_func():
    user_socket=request.environ.get("wsgi.websocket") #type:WebSocket
    user_socket_lst.append(user_socket)
    print(user_socket) ##<geventwebsocket.websocket.WebSocket object at 0x0000000003A48F50>
    while 1:
        msg=user_socket.receive() # 等待接收客户端发送过来的消息
        for user in user_socket_lst:
            if user==user_socket: ##不看自己的信息
                continue
            try: ##有可能有的退出造成ws连接关掉
                user.send(msg)
            except:
                continue
@app.route('/group')
def group():
    return render_template("group_pp.html")
if __name__ == '__main__':
    http_serve = WSGIServer(("0.0.0.0",9003), application=app, handler_class=WebSocketHandler)
    http_serve.serve_forever()
