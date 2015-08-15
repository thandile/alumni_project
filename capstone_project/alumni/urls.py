"""alumni URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views

# , include(admin.site.urls)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^profile/$', views.create_profile, name='create_profile'),
    url(r'^login/$', views.log_in, name='login')

    # add events, etc here later on...

]
