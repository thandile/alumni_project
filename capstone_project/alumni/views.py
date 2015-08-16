from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from alumni.models import Profile
from django.http import HttpResponseRedirect
from django import forms

<<<<<<< HEAD
from django.core.urlresolvers import reverse
# from settings import MEDIA_ROOT, MEDIA_URL

import autocomplete_light as AL
=======

>>>>>>> 67a84fbd8331f19adfc8d34a392a89c50ae74f99

from alumni import models
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

class UserForm(forms.Form):
        username = forms.CharField(max_length=50)
        email = forms.EmailField(max_length=50)
        password = forms.CharField(max_length=32, widget=forms.PasswordInput)
        first_name = forms.CharField(max_length=50, label = "first name")
        last_name = forms.CharField(max_length=50, label = "last name")


class ProfileForm(forms.Form):
        degree = forms.CharField(max_length=50)
        grad_year = forms.IntegerField(label= "graduation year")
        city = forms.CharField(max_length=50)
        country = forms.CharField(max_length=50)

<<<<<<< HEAD
class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('title', 'text')

def create(request):
	form = UserForm()
	if request.method == "POST":
=======
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

'''
from forms import UserForm

def lexusadduser(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(new_user)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect('main.html')
    else:
        form = UserForm() 

    return render(request, 'adduser.html', {'form': form}) 
'''


def create(request):
    form = UserForm()
    if request.method == "POST":
>>>>>>> 67a84fbd8331f19adfc8d34a392a89c50ae74f99
		# then they are sending data, create a new user
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
<<<<<<< HEAD
            #login(new_user)
            return HttpResponse("User successfully created.")
	else:
		# they are requesting the page, give 
		form = UserForm()
	return render(request, '../templates/alumni/create.html', {'form': form})
=======
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, "../templates/alumni/toProfile.html", {'userid' : new_user.id, 'username' : new_user.first_name})
    else:
        # they are requesting the page, give
        form = UserForm()
    return render(request, '../templates/alumni/create.html', {'form': form})

>>>>>>> 67a84fbd8331f19adfc8d34a392a89c50ae74f99

def index(request):
    return HttpResponse("Hello, world. You're at the alumni index.")

<<<<<<< HEAD
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

'''
# do want a function to make new posts called post though
def post(request, post_pk):
    """Display a post form."""
    subject = Thread.objects.get(pk=post_pk).title
    return render_to_response("forum/post.html", add_csrf(request, subject=subject, title=title))

'''

# Django's CreateView, ListView, UpdateView and DeleteView should be used for posting new threads, comments, etc...
# these use 'default' names for their html templates 
# http://riceball.com/d/content/django-18-minimal-application-using-generic-class-based-views
# e.g. a list view will be something like templates/alumni/forum_list.html (templates/appname/model_list.html)

=======

def logout_view(request):
    logout(request)


def create_profile(request):  #create profile
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
        return render(request, '../templates/alumni/profile.html', {'name' : name, 'surname' : surname, 'email' : email, 'city': city, "country": country, "degree" : degree, "grad_year": grad_year} )


def view_profile(request):
#view profile info
    if request.method =="POST":
        pass
    else:
        form = ProfileForm()
        user = request.user
        user_info = Profile.objects.get(user_id =user.id)
        form.name = user.first_name
        form.surname = user.last_name
        form.email = user.email
        form.city = user_info.city
        form.country = user_info.country
        form.degree = user_info.degree
        form.grad_year = user_info.grad_year
        return render(request, '../templates/alumni/createProfile.html', {'form': form})

        #return render(request, '../templates/alumni/profile.html', {'name' : name, 'surname' : surname, 'email' : email, 'city': city, "country": country, "degree" : degree, "grad_year": grad_year} )

    if request.method == 'POST':
           degree = forms.CharField(required = True)
           city = forms.CharField(required = True)
           grad_year = forms.DateTimeField(required = True)
           country = forms.CharField(required = True)
           profile = Profile(city = request.POST.get("city"), country = request.POST.get("country"), \
           degree = request.POST.get("degree"), grad_year = request.POST.get("grad_year"), user_id =2)#,\
                        #photo = request.FILES['photo']) #link profile to user
           profile.save()
           return HttpResponse("Your profile has been Edited")




def log_in(request):
    log_in = LoginForm()
    if request.method == "POST":
        log_in = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        return render(request,'../templates/alumni/homepage.html', {'username' : username})
    else:
        log_in = LoginForm()
        return render(request, '../templates/alumni/login.html', {'form':log_in})


def home(request):
    return render(request, '../templates/alumni/homepage.html')
>>>>>>> 67a84fbd8331f19adfc8d34a392a89c50ae74f99
