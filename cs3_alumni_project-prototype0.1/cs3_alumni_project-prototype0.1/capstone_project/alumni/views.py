from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
# edit this::
from alumni.models import Profile as Profile
from alumni import models
from django.http import HttpResponseRedirect
from django import forms

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.core.mail import EmailMessage
class UserForm(forms.Form):
        username = forms.CharField(max_length=50)
        email = forms.EmailField(max_length=50)
        password = forms.CharField(max_length=32, widget=forms.PasswordInput)
        first_name = forms.CharField(max_length=50, label = "First Name")
        last_name = forms.CharField(max_length=50, label = "Last Name")


class ProfileForm(forms.Form):
        degree = forms.CharField(max_length=50)
        grad_year = forms.IntegerField(label= "Graduation Year")
        city = forms.CharField(max_length=50)
        country = forms.CharField(max_length=50)

class EditProfileForm(forms.Form):
     first_name = forms.CharField(max_length=50, label = "First Name")
     last_name = forms.CharField(max_length=50, label = "Last Name")
     degree = forms.CharField(max_length=50)
     grad_year = forms.IntegerField(label= "Graduation Year")
     city = forms.CharField(max_length=50)
     country = forms.CharField(max_length=50)
	 
class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('title', 'text')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

def create(request):
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
            return render(request, "../templates/alumni/toProfile.html", {'userid' : new_user.id, 'username' : new_user.first_name})
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
                          user_id = user.id )
        profile.save()
        #send email
        email = EmailMessage('Hello', 'World', to=[ user.email])
        email.send()

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
#edit profile
def edit_profile(request):

    user = User.objects.latest('pk')
    user_info = Profile.objects.get(user_id=user.id)

    name = user.first_name
    surname = user.last_name
    email = user.email
    city = user_info.city
    country = user_info.country
    degree = user_info.degree
    grad_year = user_info.grad_year

    edit_form = EditProfileForm(request.POST or None, initial={'name' : name, 'surname' : surname, 'email' : email, 'city': city, "country": country, "degree" : degree, "grad_year": grad_year})

    if request.method == "POST":

        if form.is_valid():

            user.name = request.POST['first_name']
            user.surname = request.POST['surname']
            user.email = request.POST['email']
            user_info.city = request.POST['city']
            user_info.country = request.POST['country']
            user_info.degree = request.POST['degree']
            user_info.grad_year = request.POST['grad_year']
            edit_form.save()
            return HttpResponseRedirect('%s'%(reverse('profile')))
    context = {"form" : form}


    return render(request, '../templates/alumni/editProfile.html', context)

def view_profile(request):
#view profile info
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
