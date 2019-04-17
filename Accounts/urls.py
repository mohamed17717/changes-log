from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^$', views.Home, name='home'),
    # url(r'^login/$', views.LoginView.as_view(template_name= 'login.html'), name='login'),
    # url(r'^logout/$', views.Logout, name='logout'),

    url(r'^login/$', views.Login, name='login'),
    url(r'^logout/$', views.Logout, name='logout'),
]