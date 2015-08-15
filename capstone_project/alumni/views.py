from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django import forms

from django.core.urlresolvers import reverse
# from settings import MEDIA_ROOT, MEDIA_URL

import autocomplete_light as AL

from alumni import models

# Create your views here.

'''
class UserCreationForm(forms.Form):
	# instead of autocomplete light, see the following

	# http://stackoverflow.com/questions/11287485/taking-user-input-to-create-users-in-django
	
	user = AL.ModelMultipleChoiceField(autocomplete='UserAutocomplete')
'''

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')#, 'name', 'surname')

def create(request):
	form = UserForm()
	if request.method == "POST":
		# then they are sending data, create a new user
		form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            #login(new_user)
            return HttpResponse("User successfully created.")
            # redirect, or however you want to get to the main view
            #return HttpResponseRedirect('index.html')
	else:
		# they are requesting the page, give 
		form = UserForm()
	return render(request, '../templates/alumni/create.html', {'form': form})
#return HttpResponse("You're looking at question %s." % question_id)

def index(request):
    return HttpResponse("Hello, world. You're at the alumni index.")


def main(request):
    # Main listing - all forums
    forums = models.Forum.objects.all()
    return render(request, "../templates/alumni/main.html", dict(forums=forums, user=request.user))

# 
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


def forum(request, pk):
    # listing of threads in a particular forum
    threads = Thread.objects.filter(forum=pk).order_by("-created")
    threads = make_paginator(request, threads, 20)
    return render(response, "../templates/alumni/forum.html", add_csrf(request, threads=threads, pk=pk))

# Django's CreateView, ListView, UpdateView and DeleteView should be used for posting new threads, comments, etc...
# these use 'default' names for their html templates 
# http://riceball.com/d/content/django-18-minimal-application-using-generic-class-based-views
# e.g. a list view will be something like templates/alumni/forum_list.html (templates/appname/model_list.html)

