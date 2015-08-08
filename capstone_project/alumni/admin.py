from django.contrib import admin

from .models import Profile, Job, Advert, Event

# Register your models here.
admin.site.register(Profile)
admin.site.register(Job)
admin.site.register(Advert)
admin.site.register(Event)
