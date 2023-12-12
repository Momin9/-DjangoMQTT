from django.urls import path
from .views import MqttPublishView

urlpatterns = [
    path('', MqttPublishView.as_view(), name='mqtt-publish'),

]
