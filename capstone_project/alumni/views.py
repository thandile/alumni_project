from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage
from django.core.mail import send_mail, send_mass_mail
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.core.exceptions import *
import datetime,calendar
from datetime import  date
from django.contrib.auth.models import User
from django.template import RequestContext
from alumni.models import *
from alumni import models
from django import forms
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
import re
from django.db.models import Q

class UserForm(forms.Form):
        #username = forms.CharField(max_length=50)
        first_name = forms.CharField(max_length=50, label = "First Names")
        last_name = forms.CharField(max_length=50, label = "Last Names")
        email = forms.EmailField(max_length=50, label= "Email")
        password = forms.CharField(max_length=32, widget=forms.PasswordInput, min_length=4, label="Password")

class ProfileForm(forms.Form):
        degree = forms.CharField(max_length=50)
        grad_year = forms.ChoiceField(choices=[(x,x) for x in range(1970, 2016)])
        city = forms.CharField(max_length=50)
        country = forms.CharField(max_length=50)

class EditProfileForm(forms.Form):
     first_name = forms.CharField(max_length=50, label = "First Name")
     last_name = forms.CharField(max_length=50, label = "Last Name")
     email = forms.EmailField(max_length=50)
     degree = forms.CharField(max_length=50)
     grad_year = forms.IntegerField(label= "Graduation Year")
     city = forms.CharField(max_length=50)
     country = forms.CharField(max_length=50)


class SearchForm(forms.Form):
    search_item = forms.ChoiceField(choices = [('-',''),('1','User'),('2','Graduation Year'),('3','Degree'),\
                                               ('4', 'Company'), ('5', 'Job'),('6','Physical Location')], label="Search")


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post # forms.ModelForm allows for creation of form based on the object's definition in models. (because it's a ModelForm it uses this metadata)
        # using sensible help_text tags in the model object itself, since they'll be displayed to the html form with this method 
        fields = ('title', 'text') # specify the fields of Post model actually desired in this form

# TODO
# NB - current implementation being built requires a thread to be created AND a post to be created seperately
# If a user is creating a new thread, then it would be sensible to have a form that will produce BOTH A THREAD AND A POST at the same time!
# useful reference: http://stackoverflow.com/questions/15889794/creating-one-django-form-to-save-two-models
class ThreadForm(forms.ModelForm):
    class Meta:
        model = models.Thread
        # note forum should be automatically deduced (i.e. NOT a form field), since threads can only be made within forum x
        fields = ('title',) 

class AdvertForm(forms.ModelForm):
    class Meta:
        model = models.Advert
        # fields like creating user, created date, last_updated_date should be automatically figured and NOT presented to the user on the form!
        fields = ('title', 'description', 'annual_salary', 'description', 'closing_date','contact_details', 'reference', )

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class EventsForm(forms.Form):
    title = forms.CharField(max_length=100)
    event_type = forms.ChoiceField(choices=[('-',''),('reunion', 'reunion'), ("party", "party"), ("colloquim", "colloquim")])
    description = forms.CharField(max_length=140)
    year = forms.ChoiceField(choices = [(x,x) for x in range (2015,2017)])
    month = forms.ChoiceField(choices = [('-',''),('1','January'),('2','February'),('3', 'March'),('4','April'),('5','May'),\
                                         ('6','June'),('7','July'),('8', 'August'),('9','September'),('10','October'),\
                                         ('11','November'),('12','December')])
    day = forms.ChoiceField(choices = [(x,x) for x in range(1, 31)])
                            #[('1', "Monday"), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', "Thursday"), \
                                       #('5', "Friday"), ('6', 'Saturday'), ('7', "Sunday")])
    street = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)

class EditEventsForm(forms.Form):
    title = forms.CharField(max_length=100)
    event_type = forms.ChoiceField(choices=[('-',''),('reunion', 'reunion'), ("party", "party"), ("colloquim", "colloquim")])
    description = forms.CharField(max_length=140)
    year = forms.ChoiceField(choices = [(x,x) for x in range (2015,2017)])
    month = forms.ChoiceField(choices = [('-',''),('1','January'),('2','February'),('3', 'March'),('4','April'),('5','May'),\
                                         ('6','June'),('7','July'),('8', 'August'),('9','September'),('10','October'),\
                                         ('11','November'),('12','December')])
    day = forms.ChoiceField(choices = [('-',''),('1', "Monday"), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', "Thursday"), \
                                       ('5', "Friday"), ('6', 'Saturday'), ('7', "Sunday")])
    street = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)


'''def create(request):    #creating new user
    form = UserForm()
    if request.method == "POST":
		# then they are sending data, create a new user
        form = UserForm(request.POST)
        if form.is_valid():
            #database = MySQLdb.connect (host="localhost", user = "alumni", passwd = "redtablefan", db = "alumni")
            cursor = connection.cursor()
            #count = cursor.fetchall()
            username = cursor.execute('SELECT COUNT(*) FROM auth_user') +1
            new_user = User.objects.create_user(username=username, name =request.POST['first_name'], \
                        surname = request.POST['last_name'], password= request.POST['password'],email= request.POST['eamil'])
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            #send email
            email = EmailMessage('Hello', 'World', to=[ request.POST['email']])
            email.send()
            return render(request, "../templates/alumni/toProfile.html", {'userid' : new_user.id, 'username' : \
                new_user.first_name})
        #send email

    else:
        # they are requesting the page, give
        form = UserForm()
        return render(request, '../templates/alumni/create.html', {'form': form})

'''


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def search(request):  #searching function
    query_string = ''
    found_entries = None
    found = None
    
    searchText = normalize_query(request.GET['q'])
    
    print "**************************************************************************************"
    print "searchText is ", searchText
    print request.GET['search_item']
    print "**************************************************************************************"
    
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        if request.GET['search_item'] == "1":
            # use __in for exact matches and use __contains for "LIKE"
            matches = User.objects.filter(Q(first_name__contains=searchText) | Q(email__contains=searchText) | Q(last_name__contains=searchText))
            found = make_paginator(request, matches, 20)
            #found_entries = User.objects.filter(entry_query)
            #found = return_search_items("auth_user", found_entries)

        if request.GET['search_item'] == "2" or request.GET['search_item'] == "3" or request.GET['search_item'] == "6":
            '''
            entry_query = get_query(query_string, ['degree', 'grad_year', 'city', 'country'])
            found_entries = Profile.objects.filter(entry_query)
            found =  return_search_items("alumni_profile", found_entries)
            '''
            matches = Profile.objects.filter(Q(degree__contains=searchText) | Q(grad_year__contains=searchText) | Q(city__contains=searchText) | Q(country__contains=searchText))
            '''
            this is giving problems - I think integers field (grad_year) may need to be checked seperately
            '''
            found = make_paginator(request, matches, 20)
        if request.GET['search_item'] == "4":
            '''
            entry_query = get_query(query_string, ['company_name', 'job_desc', 'job_title'])
            found = found_entries = Job.objects.filter(entry_query)
            found = return_search_items("alumni_job", found_entries)
            '''
            matches = Job.objects.filter(Q(company_name__contains=searchText) | Q(job_desc__contains=searchText) | Q(job_title__contains=searchText))
            found = make_paginator(request, matches, 20)
        if request.GET['search_item'] == "5":
            '''
            entry_query = get_query(query_string, ['city', 'country', 'title', 'description', 'reference'])
            found_entries = Advert.objects.filter(entry_query)
            found = return_search_items("alumni_advert", found_entries)
            '''
            matches = Advert.objects.filter(Q(city__contains=searchText) | Q(country__contains=searchText) | Q(title__contains=searchText) | Q(description__contains=searchText) | Q(reference__contains=searchText))
            found = make_paginator(request, matches, 20)
    
    return render_to_response('../templates/alumni/search.html',
                          { 'query_string': query_string, 'found_entries': found },
                          context_instance=RequestContext(request))

def return_search_items(search_model, found_entries):
    items=[]
    for i in found_entries:
        id = str(i)
        #ids = int(id)
        #id = found_entries[i]
        cursor = connection.cursor()
        if search_model == "auth_user":
            cursor.execute('SELECT first_name, last_name, email FROM ' + search_model + ' where id = ' + id)
        elif search_model == "alumni_advert":
            cursor.execute('SELECT title, description, city, country, reference FROM ' + search_model + ' where pk = ' + id)
        elif search_model == "alumni_profile":
            cursor.execute('SELECT degree, grad_year, city, country FROM ' + search_model + ' where pk = ' + id)
        elif search_model == "alumni_job":
            cursor.execute('SELECT company_name, job_decs, job_title FROM ' + search_model + ' where pk = ' + id)
        items.append(cursor.fetchall())
    return items

def index(request):
    return HttpResponse("Hello, world. You're at the alumni index.") # TODO: get rid of this!


def main(request):
    # Main listing - all forums
    forums = models.Forum.objects.all()
    return render(request, "../templates/alumni/main.html", dict(forums=forums, user=request.user))


def add_csrf(request, **kwargs):
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d

def advert(request): # (i.e. post a single advert)
    if request.method == "POST":
        form = AdvertForm(request.POST)
        if form.is_valid():
            advert = Advert(**form.cleaned_data)
            advert.creating_user = request.user
            # redirect them back to careers listing
            # return render_to_response("../templates/alumni/careers.html", add_csrf(request, adverts=adverts))
            advert.save()
            return careers(request)
    else:
        form = AdvertForm()
    return render(request, "../templates/alumni/advert.html", add_csrf(request, form = form))

def advert_details(request, advert_pk):
    advert = models.Advert.objects.filter(pk=advert_pk)[0]
    return render_to_response("../templates/alumni/advertDetails.html", add_csrf(request, advert = advert))

def careers(request): # jobAdverts / careers (list of them)
    adverts = models.Advert.objects.all()
    adverts = make_paginator(request, adverts, 20)
    return render_to_response("../templates/alumni/careers.html", add_csrf(request, adverts=adverts))

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

# intentionally only allow for new forums to be created via the admin web backend. we need to dictate the terms of the discourse!
# regular joe users should be allowed to create threads and posts within the exsisting forums (of course)
def forum(request, forum_pk):
    # listing of threads in a particular forum
    threads = models.Thread.objects.filter(forum=forum_pk).order_by("-created_date")
    threads = make_paginator(request, threads, 20)
    #return render(request, "../templates/alumni/forum.html", add_csrf(request, threads=threads, pk=forum_pk))
    return render_to_response("../templates/alumni/forum.html", add_csrf(request, threads=threads, pk=forum_pk))

def thread(request, thread_pk):
    # listing of threads in a particular forum
    posts = models.Post.objects.filter(thread=thread_pk).order_by("created_date")
    posts = make_paginator(request, posts, 20)
    #return render(response, "../templates/alumni/thread.html", add_csrf(request, posts=posts, pk=thread_pk))
    return render_to_response("../templates/alumni/thread.html", add_csrf(request, posts=posts, pk=thread_pk))

# don't need a post listing function here, posts are not individual urls here, just a components of thread urls 
# the post function is used for creating a post however
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
            
            # DRY violation, but thread object not callable? better way?
            posts = models.Post.objects.filter(thread=thread_pk).order_by("created_date") # want most recent threads first, but posts should be chronological
            posts = make_paginator(request, posts, 20)
            return render_to_response("../templates/alumni/thread.html", add_csrf(request, posts=posts, pk=thread_pk))
            
            # return thread(request, thread.pk)
    else:
        # they are requesting the page / they want to post some classic vitriol
        form = PostForm()
        return render(request, '../templates/alumni/newpost.html', {'form': form})

def create_new_thread(request, forum_pk):
    # creates a thread *and* an initial post in that thread
    forum = models.Forum.objects.filter(pk=forum_pk)[0]
    if request.method == "POST":
        thread_form = ThreadForm(request.POST)
        post_form = PostForm(request.POST)
        if thread_form.is_valid() and post_form.is_valid():
            thread = models.Thread(**thread_form.cleaned_data)
            thread.forum = forum
            thread.creating_user = request.user
            thread.save()
            post = models.Post(**post_form.cleaned_data)
            post.thread = thread
            post.creating_user = request.user
            post.save()
            # go into the newly made thread
            return thread(request, thread.pk)
    else:
        thread_form = ThreadForm()
        post_form = PostForm()
    # url_path = '../templates/alumni/newthread'+ forum.pk +'.html'
    return render(request, '../templates/alumni/newthread.html', {'thread_form': thread_form, 'post_form': post_form})
    # return render(request, url_path, {'thread_form': thread_form, 'post_form': post_form})

# Django's CreateView, ListView, UpdateView and DeleteView should be used for posting new threads, comments, etc...
# these use 'default' names for their html templates 
# http://riceball.com/d/content/django-18-minimal-application-using-generic-class-based-views
# e.g. a list view will be something like templates/alumni/forum_list.html (templates/appname/model_list.html)

def spam_those_poor_suckers(subject, message, from_email = None, suckers = None):
    # a function to send mass emails to users
    # see https://docs.djangoproject.com/en/1.8/ref/contrib/auth/ for email_user()  
    if from_email is None:
        from_email = r'unreachable@dontbother.com'
    if suckers is None:
        suckers = models.User.objects.all()
    # make a list of emails from 'suckers' (i.e. recipient_list)
    recipients = []
    for spamee in suckers:
        recipients.append(spamee.email)
        spamee.email_user(subject, message)
    '''
    print recipients, type(recipients)
    # send_mass_mail(datatuple, fail_silently=False, auth_user=None, auth_password=None, connection=None)
    # datatuple is a tuple in which each element is in this format: (subject, message, from_email, recipient_list)
    datatuple = (subject, message, from_email, recipients)
    send_mass_mail(datatuple)
    '''

# display the editProfile form of some user Y to some user X. User X can 'suggest' what the field values should be
# user Y gets a email with the suggested edits and is invited to go update their profile 
# could (somehow) possible give user Y option to approve changes instead of having them edit it manually? ...
def send_proxy_info(request, editee_id):
    # editee - i.e. receiver of the edits
    editee = User.objects.get(pk=editee_id)
    editee_profile = Profile.objects.get(user_id=editee_id)
    name = editee.first_name
    surname = editee.last_name
    email = editee.email
    city = editee_profile.city
    country = editee_profile.country
    degree = editee_profile.degree
    grad_year = editee_profile.grad_year
    edit_form = EditProfileForm(request.POST or None, initial={'name' : name, 'surname' : surname, 'email' : email, 'city': city, "country": country, "degree" : degree, "grad_year": grad_year})

    if request.method == "POST":
        if edit_form.is_valid():

            editee.name = request.POST['first_name']
            editee.surname = request.POST['surname']
            editee.email = request.POST['email']
            editee_profile.city = request.POST['city']
            editee_profile.country = request.POST['country']
            editee_profile.degree = request.POST['degree']
            editee_profile.grad_year = request.POST['grad_year']
            # DO NOT SAVE THE EDITED FORM, SEND THE FORM AS AN EMAIL to user X
            
            # only email a user about changes if there are actually changes to begin with!
            if edit_form.has_changed():
                message = str(request.user.first_name) + " " + str(request.user.last_name) + " has suggested the following changes to your profile: " + '\n\r'
                for field in edit_form.changed_data:
                    message += field + edit_form[field] + '\n\r'
                spam_those_poor_suckers("Suggested edits to your Profile!", message, from_email = None, suckers = [editee] )
            
            # for now redirect to the same place as edit_progile would i.e. user Y's detials
            # may also want to give user X a notification that user Y will get an email !
            # this could change to go back to 'search listing' however 
            return HttpResponseRedirect('%s'%(reverse('profile')), context = {"form" : edit_form})

    return render(request, '../templates/alumni/editProfile.html', context)


# url(r'^profile/$', views.create_profile, name='create_profile')
def create_profile(request):  #create profile
    user = request.user
    prof_form = ProfileForm()
    if request.method == "POST":
        prof_form = ProfileForm(request.POST)
        profile = Profile(city = request.POST.get("city"), country = request.POST.get("country"),
                    degree = request.POST.get("degree"), grad_year = request.POST.get("grad_year"),
                    user_id = user.id)
        profile.save()

        #send email
        #email = EmailMessage('Hello', 'World', to=[ user.email])
        #email.send()
        user_info = Profile.objects.get(user_id=user.id)
        name = user.first_name
        surname = user.last_name
        email = user.email
        city = user_info.city
        country = user_info.country
        degree = user_info.degree
        grad_year = user_info.grad_year
        search = SearchForm()
        #send_email(user.email, "Test", "Hello world")
        return render(request, '../templates/alumni/profile.html', {'search': search, 'name' : name, 'surname' : surname, 'email' : email, 'city': city, "country": country, "degree" : degree, "grad_year": grad_year} )
    else:
        prof_form = ProfileForm()
        search = SearchForm()
        return render(request, '../templates/alumni/createProfile.html', {'form': prof_form, 'search' : search})


def profile(request):   #view profile info
        #prof = Profile.objects.get(pk=id)
        user = request.user
        #if Profile.objects.get( user_id =user.id):
        if request.method == "POST" and request.POST.get("save"):
            prof_form = ProfileForm(request.POST)
            profile = Profile(city = request.POST.get("city"), country = request.POST.get("country"),
                        degree = request.POST.get("degree"), grad_year = request.POST.get("grad_year"),
                        user_id = user.id)
            
            # profile.save() #? 

            #send email
            #email = EmailMessage('Hello', 'World', to=[ user.email])
           # email.send()
            user_info = Profile.objects.get(user_id=user.id)
            name = user.first_name
            surname = user.last_name
            email = user.email
            city = user_info.city
            country = user_info.country
            degree = user_info.degree
            grad_year = user_info.grad_year
            search = SearchForm()
            #send_email(user.email, "Test", "Hello world")
            return render(request, '../templates/alumni/profile.html', {'search': search, 'name' : name, 'surname' : surname, 'email' : email, 'city': city, "country": country, "degree" : degree, "grad_year": grad_year} )

        try:
            user_info = Profile.objects.get( user_id =user.id)
            name = user.first_name
            surname = user.last_name
            email = user.email
            city = user_info.city
            country = user_info.country
            degree = user_info.degree
            grad_year = user_info.grad_year
            search = SearchForm()
            return render(request, '../templates/alumni/profile.html', {'id' : user_info.id, 'search' : search, 'name' : name, 'surname' : surname, 'email' : email,\
                                                                        'city': city, "country": country, "degree" : degree, \
                                                                        "grad_year": grad_year} )
        except:
            prof_form = ProfileForm()
            search = SearchForm()
            return render(request, '../templates/alumni/createProfile.html', {'form': prof_form, 'search' : search})

def view_profile(request): # view profile info
    user = request.user
    prof_form = ProfileForm()
    if request.method == "POST":
        prof_form = ProfileForm(request.POST)
        # create the profile
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
        # view the profile
        prof_form = ProfileForm()
        return render(request, '../templates/alumni/createProfile.html', {'form': prof_form})

'''
def send_email(recipient, subject, body):
    import smtplib
    sender = 'csalumniuct@gmail.com'
    password = 'alumniteam4'
    to = [recipient]
    subject = subject
    text = body

    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (sender, ", ".join(to), subject, text)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to, message)
        server.close()
        print ('successfully sent the mail')
    except:
        print ("failed to send mail")
'''

def edit_profile(request, id):    #complete editing
    if request.method == "POST" and request.POST.get('edit'):
        profile = Profile.objects.get(pk=id)
        user = request.user
        prof = EditProfileForm(initial={'first_name' : user.first_name, 'last_name' : user.last_name,'email' : user.email, 'city': profile.city, "country": profile.country, "degree" : profile.degree, \
                                        "grad_year": profile.grad_year})
        return render(request, '../templates/alumni/editProfile.html', {'form' : prof})
    elif request.method == "POST" and request.POST.get('save'):
        user = request.user
        prof = EditProfileForm(request.POST)
        city = request.POST['city']
        country = request.POST['country']
        degree = request.POST['degree']
        grad_year = request.POST['grad_year']
        user_name = request.POST['first_name']
        user_lastname = request.POST['last_name']
        user_email = request.POST['email']
        prof = Profile.objects.get(pk=id)
        prof.degree = degree
        prof.grad_year = grad_year
        prof.city = city
        prof.country = country
        #profile = Profile(degree = degree, grad_year = grad_year, city = city, country = country)
        user.first_name = user_name
        user.last_name = user_lastname
        user.email = user_email
        user.save()
        prof.save()
        return render(request, '../templates/alumni/profile.html', {'name':user_name, 'surname' : user_lastname,'email':user_email, 'grad_year':grad_year, 'degree':degree, \
                                                                          'city':city, 'country': country} )

def log_in(request):
    log_in = LoginForm()
    if request.method == "POST" and request.POST.get('login'):
        log_in = LoginForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        userid = User.objects.get(email=email)
        username = userid.id
        user = authenticate(username=username, password=password)
        login(request, user)
        return render(request,'../templates/alumni/homepage.html', {'username' : username})
    elif request.method == "POST" and request.POST.get('newUser'):
        form = UserForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            #count = cursor.fetchall()
            cursor.execute('SELECT COUNT(*) FROM auth_user')
            num = cursor.fetchall()
            username = num[0][0] +1
            new_user = User.objects.create_user(username=username, first_name =request.POST['first_name'], \
                        last_name = request.POST['last_name'], password= request.POST['password'],email= request.POST['email'])
            #new_user = User.objects.create_user(**form.cleaned_data)
            username = username
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            #add_csrf(request, posts=posts, pk=thread_pk)
            return render(request, "../templates/alumni/toProfile.html", {'userid' : new_user.id, 'username' : new_user.first_name})
            #return render(request, "../templates/alumni/toProfile.html", add_csrf(request, 'userid'=new_user.id, 'username'=new_user.first_name))
    elif request.method == "GET":
        logout(request)
        log_in = LoginForm()
        sign_up = UserForm()
        return render(request, '../templates/alumni/login.html', {'form':log_in, 'signupForm' : sign_up})
'''
def newsfeed(request, num_items=None):
    if num_items is None:
        num_items = 2
    # get's latest 'num_items' events and adverts (could also add forum posts)
    events = models.Event.objects.all().order_by('created_date')[:num_items]
    adverts = models.Advert.objects.all().order_by('created_date')[:num_items]
    # posts = models.Posts.objects.all().order_by('created_date')
    return render(request, '../templates/alumni/newsfeed.html', {'events':events, 'adverts' : adverts})
'''
def home(request):
    num_items = 3
    new_events = Event.objects.all().order_by('-created_date')[:num_items]
    new_adverts = Advert.objects.all().order_by('-created_date')[:num_items]
    # posts = models.Posts.objects.all().order_by('created_date')[:num_items]
    new_events = make_paginator(request, new_events, 20)
    new_adverts = make_paginator(request, new_adverts, 20)
    #posts = make_paginator(request, posts, 20)
    return render(request, '../templates/alumni/homepage.html', {'events':new_events, 'adverts' : new_adverts, 'test' : ['HTML','REALLY','SUCKS']})
    # add_csrf(
    # return render_to_response('../templates/alumni/homepage.html', add_csrf(request, 'context_events' = new_events, 'context_adverts' = new_adverts))

def create_events(request):  #create events
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
        return render(request, '../templates/alumni/display_event.html', { 'id' : event.id, 'title':title, 'event_type':event_type, \
                                                                          'description':description, 'year': year, \
                                                                        'month':month, 'day':day, 'street':street,\
                                                                          'city':city, 'country':country})
    else:
        events = EventsForm()
        return render(request, '../templates/alumni/create_event.html', {'form':events})


def events(request):  #display events
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

    if request.method == "POST" and request.POST.get('edit'):

        event = Event.objects.get(pk=id)
        event = EventsForm(initial={'title' : event.title, 'event type' : event.event_type, 'description' : event.description, \
                                     'year' : event.year, 'month' : event.month, 'day' : event.day, \
                                    'street' : event.street, 'city' : event.city, 'country' : event.country})
        return render(request, '../templates/alumni/edit_event.html', {'form' : event})
    elif request.method == "POST" and request.POST.get('save'):
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
        event_del = Event.objects.get(pk=id)
        event_del.delete()
        event = Event(creating_user = user, title = title, event_type = event_type, description = description, \
                      year = year, month = month, day = day, street = street, city = city, country = country)
        event.save()
        return render(request, '../templates/alumni/display_event.html', { 'id' : event.id, 'title':title, 'event_type':event_type, \
                                                                          'description':description, 'year': year, \
                                                                        'month':month, 'day':day, 'street':street,\
                                                                          'city':city, 'country':country})
