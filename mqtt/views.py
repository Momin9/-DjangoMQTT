from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

from django.views.decorators.csrf import csrf_exempt


class MqttPublishView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        payload = json.loads(request.body)
        self.broadcast_message(payload)
        return JsonResponse({'status': 'Message Published'})

    def broadcast_message(self, message):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'mqtt_group',
            {
                'type': 'mqtt.message',
                'message': message['message'],
                'topic': message['topic'],
            }
        )

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')
