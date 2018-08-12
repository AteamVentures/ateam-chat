from django.conf.urls import url
from . import views


urlpatterns = [
    url('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    url('api/messages/', views.message_list, name='message-list'),
]
