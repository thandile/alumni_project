# procedures file

from django import forms
from alumni import views
from alumni import models
# from collection.forms import ContactForm

# populate the site with a bunch of stuff - to be used for testing / having something on the server
def create_community():
	pass

'''
class ProfileForm(forms.Form):
        degree = forms.CharField(max_length=50)
        grad_year = forms.ChoiceField(choices=[(x,x) for x in range(1970, 2016)])
        city = forms.CharField(max_length=50)
        country = forms.CharField(max_length=50)
'''

def form_test():
    data = {'degree': 'political science','grad_year': '1971','city': 'chigaco','country': 'Mighty Ulm'}
    data2 = {'degree': 'actual science','grad_year': '1971','city': 'chigaco','country': 'Mighty Ulm'}
    f = views.ProfileForm(data, initial=data2)
    f.has_changed()
    if f.has_changed():
    	for change in f.changed_data:
    		print "change we can belive in ", change, data2[change]

def test_changes_alert(test_sucker):
    data = {'degree': 'political science','grad_year': '1971','city': 'chigaco','country': 'Mighty Ulm'}
    data2 = {'degree': 'actual science','grad_year': '1971','city': 'chigaco','country': 'Mighty Ulm'}
    f = views.ProfileForm(data, initial=data2)
    f.has_changed()
    if f.has_changed():
        message = ""
        message = str("TEST") + " " + str("TEST") + " has suggested the following changes to your profile: " + '\n\r'
        for field in f.changed_data:
            message += str(field) + str(f[field]) + '\n\r'
        
        if test_sucker is None:
        	test_sucker = models.User.objects.filter(username="jarryd")

        views.spam_those_poor_suckers("Suggested edits to your Profile!", message, from_email = None, suckers =  test_sucker)