from channels.generic.websocket import AsyncWebsocketConsumer
import json


class WebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 发送成功消息
        await self.send(text_data=json.dumps({
            'message': '连接成功'
        }))
        await self.accept()

    async def disconnect(self, close_code):
        # 发送关闭消息
        await self.send(text_data=json.dumps({
            'message': '连接关闭'
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({
            'message': data['message']
        }))
