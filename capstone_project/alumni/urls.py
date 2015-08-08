
"""alumni URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views

# , include(admin.site.urls)

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^create/$', views.create, name = 'create'),
	# add events, etc here later on...

]
