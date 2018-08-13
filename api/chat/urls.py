# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import ChatViewSet

message_list = ChatViewSet.as_view({
    'post': 'create',
    'get': 'list',
})

message_receiver_list = ChatViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    url(r'^messages/^(?P<sender>\d+)/(?P<receiver>\d+)/$', message_list, name='message-list'),
    url(r'^messages/$', message_receiver_list, name='message-receiver'),
]
