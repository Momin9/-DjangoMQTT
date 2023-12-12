from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import paho.mqtt.client as mqtt
import json
from django.utils import timezone


class MyMqttConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # self.group_name = 'mqtt_group'
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        self.mqtt_client.username_pw_set("momin5", "Iub@12345")
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect("669b5ece37344c7f8944e682f5a860c8.s2.eu.hivemq.cloud", 8884, 60)
        self.mqtt_client.loop_start()
        self.mqtt_client.on_subscribe = self.on_subscribe
        self.mqtt_client.on_publish = self.on_publish

    async def disconnect(self, close_code):
        self.mqtt_client.disconnect()

    async def on_connect(self, client, userdata, flags, rc, properties=None):
        print("Connected with result code " + str(rc))
        client.subscribe("testtopic/1")

    async def on_subscribe(self, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    async def on_publish(self, userdata, mid, properties=None):
        print("mid: " + str(mid))

    async def on_message(self, client, userdata, msg):
        message = msg.payload.decode('utf-8')
        await self.send(text_data=json.dumps({'message': message, 'timestamp': timezone.now().isoformat()}))
        print(msg)

    # websocket connection
    async def ws_connect(self, message):
        channel_name = message.get('path').strip("/")
        await message.reply_channel.send({"accept": True})
        await async_to_sync(self.channel_layer.group_add)(
            channel_name,
            message.reply_channel.name,
        )

    #  webSocket disconnections
    async def ws_disconnect(self, message):
        channel_name = message.get('path').strip("/")
        await async_to_sync(self.channel_layer.group_discard)(
            channel_name,
            message.reply_channel.name,
        )

    # webSocket receives
    async def ws_receive(self, message):
        channel_name = message.get('path').strip("/")
        payload = json.loads(message["text"])
        print(payload, channel_name)
