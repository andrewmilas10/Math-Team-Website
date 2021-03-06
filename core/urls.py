from django.conf.urls import url
from . import views

app_name = 'core'

#these are the different url patterns that the website can access, they are called from the views.py
#file
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^post_list/$', views.post_list, name='post_list'),
    url(r'^learn/(?P<category>[0-9]+)/(?P<title>[a-zA-Z, -]+)/$', views.learn, name='learn'),
    url(r'^question_list/$', views.question_list, name ='question_list'),
    url(r'^question_list/(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^homepage$', views.homepage, name='homepage'),
    url(r'^questions/(?P<filter_by>[a-zA_Z]+)/$', views.questions, name='questions'),
    # url(r'^practice_topics/$', views.practice_topics, name='practice_topics'),
    url(r'^practice_topics/(?P<title>[a-zA_Z]+)/$', views.practice_topics, name='practice_topics'),

    url(r'^practice_topics/(?P<category>[0-9]+)/$', views.practice_topics, name='practice_topics'),
    url(r'^practice_tests/(?P<category>[0-9]+)/$', views.practice_tests, name='practice_tests'),
    url(r'^practice_topics_detail/(?P<topic>[a-zA-Z0-9, -]+)/$', views.practice_topics_detail, name='practice_topics_detail'),
    url(r'^practice_tests_detail/(?P<topic>[a-zA-Z0-9, -]+)/$', views.practice_tests_detail, name='practice_tests_detail'),
    url(r'^practice_tests_take/(?P<topic>[a-zA-Z0-9, -]+)/$', views.practice_tests_take, name='practice_tests_take'),
    url(r'^reset/(?P<topic>[a-zA-Z0-9, -]+)/(?P<category>[0-9]+)/$', views.reset, name='reset'),
    url(r'^start_timer$', views.start_timer, name='start_timer'),
    url(r'^end_timer$', views.end_timer, name='end_timer'),
    url(r'^edit_answers$', views.edit_answers, name='edit_answers'),
    url(r'^update_profiles$', views.update_profiles, name='update_profiles'),
    url(r'^progress/(?P<category>[0-9]+)/(?P<title>[a-zA-Z, -]+)/$', views.progress, name='progress')
]
