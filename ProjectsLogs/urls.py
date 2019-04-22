from django.conf.urls import url
from . import views

app_name = 'projects'
urlpatterns = [
    url(r'^$', views.Home, name='home'),
    url(r'^adminstration/$', views.Adminstration, name='adminstration'),
    url(r'^adminstration/(?P<profile_slug>[-_@\w\.]+)/add-project/$', views.AddProject, name='add_project'),
    url(r'^adminstration/(?P<project_slug>[-_@\w\.]+)/edit-project/$', views.EditProject, name='edit_project'),


    url(r'^(?P<slug>[-_@\w\.]+)/$', views.OpenProject, name='project'),
    url(r'^replay/(?P<comment_id>\d+)/$', views.SubmitCommentReplay, name='submit_comment_replay'),
    url(r'^comment/(?P<change_type>[-_@\w\.]+)/(?P<change_id>\d+)/$', views.SubmitComment, name='submit_comment'),




]