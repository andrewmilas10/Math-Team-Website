from django.conf.urls import url
from . import views

app_name = 'core'

#these are the different url patterns that the website can access, they are called from the views.py
#file
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^post_list/$', views.post_list, name='post_list'),
    url(r'^question_list/$', views.question_list, name ='question_list'),
    url(r'^question_list/(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^homepage$', views.homepage, name='homepage'),
    url(r'^questions/(?P<filter_by>[a-zA_Z]+)/$', views.questions, name='questions'),
    

]
