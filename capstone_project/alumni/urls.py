
"""alumni URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin

from alumni import views

# trouble with reverse lookups, but url pattern is correctly specified? See here: -> http://stackoverflow.com/questions/146522/how-do-i-successfully-pass-a-function-reference-to-django-s-reverse-function

# , include(admin.site.urls)
# https://docs.djangoproject.com/en/1.8/topics/http/urls/


urlpatterns = [
	# main listing 
	
	# url(r'main/', views.main, name = 'main'),
	url(r'main/', views.main, name = 'main'),
	

	url(r'^$', views.index, name = 'index'), # $:: End of String match character
	url(r'^create/$', views.create, name = 'create'), # web page is generated based on code in views.py -> Note: path will be /alumni/create/ **NOT** /create/
	# add events, etc here later on...

	# it may make sense to move forum stuff to a seperate app later...
	
	url(r'^forum/(\d+)/$', views.forum, name = 'forum'),	
	
	# url(r"^thread/(\d+)/$", views.create, name = 'thread'),
]



'''
(r"", "main"),
(r"^forum/(\d+)/$", "forum"),
(r"^thread/(\d+)/$", "thread"),
'''
