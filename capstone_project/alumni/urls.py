"""alumni URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin

from alumni import views

# references:
# trouble with reverse lookups, but url pattern is correctly specified? See here: -> http://stackoverflow.com/questions/146522/how-do-i-successfully-pass-a-function-reference-to-django-s-reverse-function
# https://docs.djangoproject.com/en/1.8/topics/http/urls/

# url patterns in this file are all prefixed by alumni/

urlpatterns = [
	#url(r'^thread/(?P<forum_pk>[0-9]+)/new/$', views.create_new_thread, name = 'create_new_thread'),	
    #url(r'^new_thread/$', views.create_new_thread, name = 'create_new_thread'),	
	#url(r'^thread/new/$', views.create_new_thread, name = 'create_new_thread'),	
    #url(r'^thread/new/(?P<forum_pk>[0-9]+)$', views.create_new_thread, name = 'create_new_thread'), #, {'forum_pk': 'forum_pk'}),	
    #url(r'^new_thread/$', views.create_new_thread, name = "create_new_thread"),
    url(r'main/', views.main, name='main'),
    url(r'^$', views.index, name='index'),  # $:: End of String match character
    url(r'^create/$', views.create, name='create'),
    # web page is generated based on code in views.py -> Note: path will be /alumni/create/ **NOT** /create/
    url(r'^forum/(?P<forum_pk>[0-9]+)/$', views.forum, name='forum'),
    url(r'^thread/(?P<thread_pk>[0-9]+)/$', views.thread, name='thread'),
    url(r'^new_thread/(?P<forum_pk>[0-9]+)/$', views.create_new_thread, name="new_thread"),
    url(r'^post/(?P<thread_pk>[0-9]+)/$', views.post, name="new_post"), # idea here is for creating a new post, NOT a listing of posts like the above
    url(r'^profile/$', views.create_profile, name='create_profile'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^user_profile/$', views.profile, name='user_profile'),
    url(r'^userprofile/$', views.profile, name='user_profile'),
    url(r'^home/$', views.home, name='home'),
    url(r'^edit_profile/$', views.view_profile, name='view_profile'),
	
	url(r'^careers/$',views.careers, name ='careers'),
	url(r'^advert/(?P<advert_pk>[0-9]+)/$',views.advert_details, name ='advert_details'),
    url(r'^advert/$',views.advert, name ='advert'),
	
	url(r'^create_event/$', views.create_events, name="create_events"),
	url(r'^events/(?P<id>\d+)/$', views.events_view, name="events_view"),
	url(r'^events/$', views.events, name="events"),
    url(r'^events/delete/(?P<id>\d+)/$', views.events_delete, name="events_delete"),
    url(r'^events/edit/(?P<id>\d+)/$', views.events_edit, name="events_edit"),
    # url(r'^thread/(?P<forum_pk>[0-9]+)/$', views.postthread, name = 'postthread'),
    # url(r"^thread/(\d+)/$", views.create, name = 'thread'),
]

'''
(r"", "main"),
(r"^forum/(\d+)/$", "forum"), <- nope.
(r"^thread/(\d+)/$", "thread"),
'''
'''
(r"^post/(new_thread|reply)/(\d+)/$", "post"),
(r"^reply/(\d+)/$", "reply"),
(r"^new_thread/(\d+)/$", "new_thread"),
'''
