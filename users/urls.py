from django.conf.urls import include, url
from users.views import LoginView, SignupView, LandingView, LogoutView, username_dup_check

urlpatterns = [
    url(r'^$', LandingView.as_view(), name='landing'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^available-username/$', username_dup_check, name='username_check'),
]
