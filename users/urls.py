from django.conf.urls import include, url
from users.views import LoginView, SignupView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
]