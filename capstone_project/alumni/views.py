from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.core.exceptions import *
import datetime,calendar
from datetime import  date
from django.contrib.auth.models import User
# edit this::
from alumni.models import *

from alumni import models
from django import forms
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.core.context_processors import csrf


class UserForm(forms.Form):
        username = forms.CharField(max_length=50)
        first_name = forms.CharField(max_length=50, label = "First Names")
        last_name = forms.CharField(max_length=50, label = "Last Names")
        email = forms.EmailField(max_length=50, label= "Email")
        password = forms.CharField(max_length=32, widget=forms.PasswordInput, min_length=4, label="Password")


class ProfileForm(forms.Form):
        degree = forms.CharField(max_length=50)
        grad_year = forms.ChoiceField(choices=[(x,x) for x in range(1970, 2016)])
        city = forms.CharField(max_length=50)
        country = forms.CharField(max_length=50)


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('title', 'text')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class EventsForm(forms.Form):
    title = forms.CharField(max_length=100)
    event_type = forms.ChoiceField(choices=[('reunion', 'reunion'), ("party", "party"), ("colloquim", "colloquim")])
    description = forms.CharField(max_length=140)
    year = forms.ChoiceField(choices = [(x,x) for x in range (2015,2017)])
    month = forms.ChoiceField(choices = [('1','January'),('2','February'),('3', 'March'),('4','April'),('5','May'),\
                                         ('6','June'),('7','July'),('8', 'August'),('9','September'),('10','October'),\
                                         ('11','November'),('12','December')])
    day = forms.ChoiceField(choices = [('1', "Monday"), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', "Thursday"), \
                                       ('5', "Friday"), ('6', 'Saturday'), ('7', "Sunday")])
    street = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)


class EditEventsForm(forms.Form):
    title = forms.CharField(max_length=100)
    event_type = forms.ChoiceField(choices=[('reunion', 'reunion'), ("party", "party"), ("colloquim", "colloquim")])
    description = forms.CharField(max_length=140)
    year = forms.ChoiceField(choices = [(x,x) for x in range (2015,2017)])
    month = forms.ChoiceField(choices = [('1','January'),('2','February'),('3', 'March'),('4','April'),('5','May'),\
                                         ('6','June'),('7','July'),('8', 'August'),('9','September'),('10','October'),\
                                         ('11','November'),('12','December')])
    day = forms.ChoiceField(choices = [('1', "Monday"), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', "Thursday"), \
                                       ('5', "Friday"), ('6', 'Saturday'), ('7', "Sunday")])
    street = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)


def create(request):    #creating new user
    form = UserForm()
    if request.method == "POST":
		# then they are sending data, create a new user
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, "../templates/alumni/toProfile.html", {'userid' : new_user.id, 'username' : \
                new_user.first_name})
    else:
        # they are requesting the page, give
        form = UserForm()
        return render(request, '../templates/alumni/create.html', {'form': form})


def index(request):
    return HttpResponse("Hello, world. You're at the alumni index.")


def main(request):
    # Main listing - all forums
    forums = models.Forum.objects.all()
    return render(request, "../templates/alumni/main.html", dict(forums=forums, user=request.user))


def add_csrf(request, **kwargs):
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d


def make_paginator(request, items, num_items):
    # Make a generic paginator usable at forum level / thread level / and on other objects 
    paginator = Paginator(items, num_items)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1
    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items

def forum(request, forum_pk):
    # listing of threads in a particular forum
    threads = models.Thread.objects.filter(forum=forum_pk).order_by("-created_date")
    threads = make_paginator(request, threads, 20)
    #return render(request, "../templates/alumni/forum.html", add_csrf(request, threads=threads, pk=forum_pk))
    return render_to_response("../templates/alumni/forum.html", add_csrf(request, threads=threads, pk=forum_pk))

def thread(request, thread_pk):
    # listing of threads in a particular forum
    posts = models.Post.objects.filter(thread=thread_pk).order_by("-created_date")
    posts = make_paginator(request, posts, 20)
    #return render(response, "../templates/alumni/thread.html", add_csrf(request, posts=posts, pk=thread_pk))
    return render_to_response("../templates/alumni/thread.html", add_csrf(request, posts=posts, pk=thread_pk))

# don't need a post listing function here, posts are NOT urls! Do have a new post function though
def post(request, thread_pk):
    form = PostForm()
    thread = models.Thread.objects.filter(pk=thread_pk)[0]
    if request.method == "POST":
        # then they are sending data, create a new user
        form = PostForm(request.POST)
        if form.is_valid():
            post = models.Post(**form.cleaned_data)
            post.thread = thread # not a form input
            post.creating_user = request.user
            post.save()

            # DRY violation, but thread object not callable? fix this later
            posts = models.Post.objects.filter(thread=thread_pk).order_by("-created_date")
            posts = make_paginator(request, posts, 20)
            return render_to_response("../templates/alumni/thread.html", add_csrf(request, posts=posts, pk=thread_pk))
            #return thread(request, thread_pk)
    else:
        # they are requesting the page, give 
        form = PostForm()
        return render(request, '../templates/alumni/newpost.html', {'form': form})

def create_new_thread():
    return HttpResponse("TODO.")

# Django's CreateView, ListView, UpdateView and DeleteView should be used for posting new threads, comments, etc...
# these use 'default' names for their html templates 
# http://riceball.com/d/content/django-18-minimal-application-using-generic-class-based-views
# e.g. a list view will be something like templates/alumni/forum_list.html (templates/appname/model_list.html)

def logout_view(request):
    logout(request)

def create_profile(request):  #create profile
    user = User.objects.latest('pk')
    prof_form = ProfileForm()
    if request.method == "POST":
        prof_form = ProfileForm(request.POST)
        profile = Profile(city = request.POST.get("city"), country = request.POST.get("country"),
                    degree = request.POST.get("degree"), grad_year = request.POST.get("grad_year"),
                    user_id = user.id)
        profile.save()
        user_info = Profile.objects.get(user_id=user.id)
        name = user.first_name
        surname = user.last_name
        email = user.email
        city = user_info.city
        country = user_info.country
        degree = user_info.degree
        grad_year = user_info.grad_year
        return render(request, '../templates/alumni/profile.html', {'name' : name, 'surname' : surname, 'email' : email, 'city': city, "country": country, "degree" : degree, "grad_year": grad_year} )
    else:
        prof_form = ProfileForm()
        return render(request, '../templates/alumni/createProfile.html', {'form': prof_form})

def profile(request):   #view profile info
    if request.method =="POST":
        pass
    else:
        user = request.user
        user_info = Profile.objects.get(user_id =user.id)
        name = user.first_name
        surname = user.last_name
        email = user.email
        city = user_info.city
        country = user_info.country
        degree = user_info.degree
        grad_year = user_info.grad_year
        return render(request, '../templates/alumni/profile.html', {'name' : name, 'surname' : surname, 'email' : email,\
                                                                    'city': city, "country": country, "degree" : degree, \
                                                                    "grad_year": grad_year} )

def view_profile(request):
#view profile info
  #def create_profile(request):  #create profile
    user = User.objects.latest('pk')
    prof_form = ProfileForm()
    if request.method == "POST":

        prof_form = ProfileForm(request.POST)
        profile = Profile(city = request.POST.get("city"), country = request.POST.get("country"),
                    degree = request.POST.get("degree"), grad_year = request.POST.get("grad_year"),
                          user_id = user.id )
        profile.save()
        user_info = Profile.objects.get(user_id=user.id)
        name = user.first_name
        surname = user.last_name
        email = user.email
        city = user_info.city
        country = user_info.country
        degree = user_info.degree
        grad_year = user_info.grad_year
        return render(request, '../templates/alumni/profile.html', {'name' : name, 'surname' : surname, 'email' : email, \
                                                                    'city': city, "country": country, "degree" : degree,\
                                                                    "grad_year": grad_year} )
    else:
        prof_form = ProfileForm()
        return render(request, '../templates/alumni/createProfile.html', {'form': prof_form})

def log_in(request):
    log_in = LoginForm()
    if request.method == "POST" and request.POST.get('login'):
        log_in = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        return render(request,'../templates/alumni/homepage.html', {'username' : username})
    elif request.method == "POST" and request.POST.get('newUser'):
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, "../templates/alumni/toProfile.html", {'userid' : new_user.id, 'username' : \
                new_user.first_name})
    else:
        log_in = LoginForm()
        sign_up = UserForm()
        return render(request, '../templates/alumni/login.html', {'form':log_in, 'signupForm' : sign_up})


def home(request):
    return render(request, '../templates/alumni/homepage.html')


def create_events(request):
    if request.method == "POST":
        user = request.user
        events = EventsForm(request.POST)
        title = request.POST['title']
        event_type = request.POST['event_type']
        description = request.POST['description']
        year = request.POST['year']
        month = request.POST['month']
        day = request.POST['day']
        street = request.POST['street']
        city = request.POST['city']
        country = request.POST['country']
        event = Event(creating_user = user, title = title, event_type = event_type, description = description, \
                      year = year, month = month, day = day, street = street, city = city, country = country)
        event.save()
        return render(request, '../templates/alumni/display_event.html', { 'title':title, 'event_type':event_type, \
                                                                          'description':description, 'year': year, \
                                                                        'month':month, 'day':day, 'street':street,\
                                                                          'city':city, 'country':country})
    else:
        events = EventsForm()
        return render(request, '../templates/alumni/create_event.html', {'form':events})


def events(request):
    if request.method == "POST" and request.POST.get('delete'):
        obj = Event.objects.get(pk=id)
        #if request.user == obj.creating_user:  delete only if creating user
        obj.delete()
        event = Event.objects.all()
        #return HttpResponse("Event deleted")
        return render(request, '../templates/alumni/events.html', {'events': event})
    else:
        event = Event.objects.all()
        return render(request, '../templates/alumni/events.html', {'events':event})


def events_view(request, id):   #view selected event
    event = Event.objects.get(pk=id)
    title = event.title
    event_type = event.event_type
    description = event.description
    year = event.year
    month = event.month
    day = event.month
    street = event.street
    city = event.street
    country = event.country
    return render(request, '../templates/alumni/display_event.html', {'id' : event.id, 'title':title, 'event_type':event_type, \
                                                                      'description':description, 'year': year, \
                                                                      'month':month, 'day':day, 'street':street, \
                                                                      'city':city, 'country':country})



def events_delete(request, id):
    if request.method == "POST" and request.POST.get('delete'):
        obj = Event.objects.get(pk=id)
        obj.delete()
        event = Event.objects.all()
        #return HttpResponse("Event deleted")
        return render(request, '../templates/alumni/events.html', {'events': event})
    else:
        event = Event.objects.all()
        return render(request, '../templates/alumni/events.html', {'events':event})

def events_edit(request, id):    #complete editing
    if request.method == "POST":
        event = Event.objects.get(pk=id)
        title = event.title
        event_type = event.event_type
        description = event.description
        year = event.year
        month = event.month
        day = event.month
        street = event.street
        city = event.street
        country = event.country
        return render(request, '../templates/alumni/display_event.html', {'events':event})
    else:
        return render(request, '../templates/alumni/edit_event.html')