from channels.generic.websocket import AsyncWebsocketConsumer
import json

class LeaderboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("leaderboard", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("leaderboard", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        await self.channel_layer.group_send(
            "leaderboard",
            {
                'type': 'leaderboard_update',
                'data': text_data_json
            }
        )

    async def leaderboard_update(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))