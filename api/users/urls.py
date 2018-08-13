# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import UsersViewSet

user_list = UsersViewSet.as_view({
    'post': 'create',
})

user_detail = UsersViewSet.as_view({
    'head': 'retrieve',
})

urlpatterns = [
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<username>[a-zA-Z0-9_]{3,32})/$', user_detail, name='user-detail'),
]
