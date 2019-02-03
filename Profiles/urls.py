from django.conf.urls import url

from . import views

app_name = 'profiles'
urlpatterns = [
    url(r'^$', views.Home, name='home'),
    url(r'^(?P<slug>[-_@\w\.]+)/$', views.OpenProfile, name='profile')
]