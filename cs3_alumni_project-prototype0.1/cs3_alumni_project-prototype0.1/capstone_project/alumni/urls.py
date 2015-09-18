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
	url(r'main/', views.main, name = 'main'),
	
	url(r'^$', views.index, name = 'index'), 			# $:: End of String match character
	url(r'^create/$', views.create, name = 'create'), 	# web page is generated based on code in views.py -> Note: path will be /alumni/create/ **NOT** /create/
	
	url(r'^forum/(?P<forum_pk>[0-9]+)/$', views.forum, name = 'forum'),	
	
	url(r'^thread/(?P<thread_pk>[0-9]+)/$', views.thread, name = 'thread'),	
	
	url(r'^new_thread/(?P<forum_pk>[0-9]+)/$', views.create_new_thread, name = "new_thread"),

	url(r'^post/(?P<thread_pk>[0-9]+)/$', views.post, name = "new_post"), # idea here is for creating a new post, NOT a listing of posts like the above

    url(r'^profile/$', views.create_profile, name='create_profile'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^userprofile/$', views.profile, name='user_profile'),
    url(r'^home/$', views.home, name='home'),
    url(r'^editProfile/$',views.edit_profile, name ='edit_profile'),
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
