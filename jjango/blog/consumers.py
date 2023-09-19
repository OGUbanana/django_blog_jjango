import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .views import autocomplete

class AutoWriteConsumer(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        post_title = text_data_json.get('post_title', '')
        
        response_generator = autocomplete(post_title)
        for response in response_generator:
            if 'choices' in response:
                try:
                    message_content = response['choices'][0]['delta']
                    json_message = json.dumps(message_content, ensure_ascii=False)
                    await asyncio.sleep(0.05)
                    await self.send(text_data=json_message)
                except Exception :
                    print('생성 완료')