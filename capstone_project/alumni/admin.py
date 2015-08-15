from django.contrib import admin

from .models import Profile, Job, Advert, Event, Forum, Thread, Post

# Register your models here.
admin.site.register(Profile)
admin.site.register(Job)
admin.site.register(Advert)
admin.site.register(Event)

admin.site.register(Forum)
admin.site.register(Thread)
admin.site.register(Post)
