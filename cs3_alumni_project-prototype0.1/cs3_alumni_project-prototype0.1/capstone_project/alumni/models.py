from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


# GRSJAR001, Jarryd Garisch, 08/08/2015

'''
# https://docs.djangoproject.com/en/1.8/topics/auth/default/
# The primary attributes of the default user are:
    username
    password
    email
    first_name
    last_name
in django there is just 'User', to create a superuser change permissions on this object instead of using a child of user
'''

'''
Solid, up-to-date, reference: http://riceball.com/d/content/django-18-minimal-application-using-generic-class-based-views

'''


class Profile(models.Model):
    user = models.ForeignKey(User, related_name='user_obj')
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    grad_year = models.IntegerField(blank=True, null=True)
    degree = models.CharField(max_length=255, blank=True, null=True)
    #company = models.CharField(max_length=255, blank=True, null=True)

    #grad_year as DeciminalField(maxDigits = 4)?
    #photo = ImageWithThumbsField(upload_to='photo', sizes=((125,125),(200,200)), null=True)
    # will  useful to have the following fields on most things:
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.city) + ', ' + str(self.country) + ', ' + str(self.degree) + ', ' + str(self.grad_year) + ', ' + str(self.user)

# instead of company on the profile itself, job object linked to a profle
class Job(models.Model): # job in the 'piece of work history' sense, not a job advert

    company_name = models.CharField(max_length=255, blank=True, null=True)
    job_desc = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True) #the reference for the company advertising?
    
    # thinking that we can grab jobs in their order of dates on the profile. 
    start_date = models.DateTimeField() #blank=True, null=True <- allow nulls?
    end_date = models.DateTimeField()
    
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return str(self.company_name) + ', '+ str(self.job_desc) + ', ' +str(self.job_title)

class Advert(models.Model): # "Jobs"
    creating_user = models.ForeignKey(User, related_name='advert_user')

    city = models.CharField(max_length=255, blank=True, null=True) # why 255? -> mySQL limit
    country = models.CharField(max_length=255, blank=True, null=True)

    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True) #the reference for the company advertising?
    
    closing_date = models.DateTimeField()
    
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return str(self.title) + ', ' + str(self.description)

class Event(models.Model):
    # foreign key should be to the user who created the original Event
    creating_user = models.ForeignKey(User, related_name='event_user')

    # location - may need to change this one.
    street = models.CharField(max_length=255, blank=True, null=True) # i.e street, road, lane, drive, etc... with a house/flat number
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    event_type = models.CharField(max_length=255, blank=True, null=True) # event type? pre-defined things such as 'Staff' + 'Public' or anything? may want to change this

    event_date = models.DateTimeField()
    
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return str(self.title) + ', ' + str(self.description)


# Forum, Thread + Post makes sense - see here: http://lightbird.net/dbe/forum1.html
# A forum has many threads. Each thread has many posts.
class Forum(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)
    
    # forum functions 
    def get_num_posts(self):
        # count the number of posts in each Thread, then sum all of them up
        return sum([t.get_num_posts() for t in self.thread_set.all()]) # Django's "_set" voodoo explained here: http://stackoverflow.com/questions/14228477/set-attributes-on-django-models

    # could add a get latest post at the forum level that checks accross all theads in *this* forum if desired later

    def get_absolute_url(self): # allows avoiding repition in html templates!
        '''Returns url where forums can be viewed on website - displayed as a *list* of forums'''
        return reverse('alumni.views.forum', kwargs={'forum_pk':self.pk})

    def __unicode__(self):
        return self.title

class Thread(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)

    forum = models.ForeignKey(Forum)
    creating_user = models.ForeignKey(User, related_name='thread_user')
    
    # thread functions
    def get_num_posts(self):
        # count the number of posts in *this* particular thread
        return self.post_set.count()

    def get_num_replies(self):
        return (self.get_num_posts()-1)

    def get_latest_post(self):
        if self.post_set.count():
            # order all posts by date of creation, return the first one
            return self.post_set.order_by("created_date")[0]

    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('alumni.views.thread', kwargs={'thread_pk':self.pk})

    def __unicode__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)

    thread = models.ForeignKey(Thread)
    creating_user = models.ForeignKey(User, related_name='post_user')
    
    text = models.TextField(max_length=10000) # The actual contents of the post itself. TEXT ONLY for now!

    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        '''Returns url to reply to a particular post, pk of the thread the post belongs is relevant'''
        return reverse('alumni.views.post', kwargs={'thread_pk':self.thread.pk})
    
    def __unicode__(self):
        return u"%s - %s - %s" % (self.creating_user, self.thread, self.title)
