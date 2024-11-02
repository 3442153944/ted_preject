import json
import tornado.ioloop
import tornado.web
import tornado.websocket
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.models import User
from django.utils import timezone
import jwt

# Security settings
SECRET_KEY = 'django-insecure-e_$uf9(uekzu)d6xr6g1lsb+im88_py@9=3n&3-hp#a(&)^g0^'

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def check_origin(self, origin):
        return True  # 允许来自任何域的请求（根据需要进行更严格的限制）

    def open(self, token):
        # 验证 JWT
        try:
            payload = AccessToken(token)
            self.user_id = payload['user_id']
            self.clients.add(self)
            print(f"WebSocket opened for user: {self.user_id}")
        except TokenError:
            self.close()  # 关闭未认证的连接

    def on_message(self, message):
        print(f"Received message: {message}")
        for client in self.clients:
            client.write_message(f"You said: {message}")

    def on_close(self):
        self.clients.remove(self)
        print(f"WebSocket closed for user: {self.user_id}")

def make_app():
    return tornado.web.Application([
        (r'/websocket', WebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)  # 监听8888端口
    tornado.ioloop.IOLoop.current().start()
