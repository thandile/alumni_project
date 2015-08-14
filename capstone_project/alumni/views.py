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
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class ProfileForm(forms.Form):
        degree = forms.CharField(max_length=50, label= "degree")
        grad_year = forms.IntegerField(label= "graduation year")
        city = forms.CharField(max_length=50)
        country = forms.CharField(max_length=50)

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
		# then they are sending data, create a new user
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            #send_mail("UCT alumni network", "You have just joined the uct alumni network", settings.EMAIL_HOST_USER, [new_user.email], fail_silently=False )

            return render(request, "../templates/alumni/toProfile.html", {'userid' : new_user.id, 'username' : new_user.first_name})
    else:
        # they are requesting the page, give
        form = UserForm()
    return render(request, '../templates/alumni/create.html', {'form': form})


def index(request):
    return HttpResponse("Hello, world. You're at the alumni index.")

def logout_view(request):
    logout(request)

def create_profile(request):  #create profile
    user = User.objects.latest('pk')
    prof_form = ProfileForm()
    if request.method == "POST":

        prof_form = ProfileForm(request.POST)
        profile = Profile(city = request.POST.get("city"), country = request.POST.get("country"),
                    degree = request.POST.get("degree"), grad_year = request.POST.get("grad_year"),
                          user_id = user.id )#, photo = request.FILES['photo']) #link profile to user
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

'''def profile(request):   #view profile info
    if request.method =="POST":
        pass
    else:
        user_info = Profile.objects.get(pk=1)
        return render(request, '../templates/alumni/profile.html', {'user_info': user_info} ) '''
