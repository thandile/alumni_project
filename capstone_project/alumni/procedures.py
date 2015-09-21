# procedures file
from django import forms
from alumni import views
from alumni import models
from datetime import date
# from collection.forms import ContactForm

# populate the site with a bunch of stuff - to be used for testing / having something on the server without JSON / Fixture 'complications' for now.
# technically, this really SHOULD be done with fixtures (if we were using REAL data) - but since all data used here is 'fake', it doesn't really matter
def create_community():
	# create some Users
    user_a = models.User(username = "AB", first_name="Ahmed", last_name="Baboosh", password = "password123", email = "ahmed.b@gmail.com")
    user_b = models.User(username = "CD", first_name="Cathy", last_name="Debreezy", password = "password123", email = "cathyb@yahoo.com")
    user_c = models.User(username = "EF", first_name="Erik", last_name="Frankopoldo", password = "password123", email = "erikthered@gmail.com") 
    user_a.save()
    user_b.save()
    user_c.save()
    # User.objects.create_user(username=username, first_name =request.POST['first_name'], last_name = request.POST['last_name'], password= request.POST['password'],email= request.POST['email'])
    # create Profiles for the above users
    profile_a = models.Profile(user = user_a, city="Garyville", country="Greater Serbia", grad_year = 2010, degree = "MCom Interpretive Finance")
    profile_b = models.Profile(user = user_b, city="Hanksville", country="Byzantium", grad_year = 2009, degree = "Hons in Pyrokinesis")
    profile_c = models.Profile(user = user_c, city="Los Pintos", country="Carpathia", grad_year = 2008, degree = "Doctor of Diagnostic Medicine") 
    profile_a.save()
    profile_b.save()
    profile_c.save()
    # create some Events (x3)
    event_a = models.Event(user = user_a, year = 2016, month = 1, day = 15, title = "Coding CARNAGE", description = "I got my first real laptop. Bought it at the five and dime. Coded till my fingers bled. Was the summer of '69", event_type = "Contest", street = "4 Great Leader Way",city="Glorious Capital of Arstortska", country="Arstortska")
    event_b = models.Event(user = user_b, year = 2016, month = 1, day = 15, title = "Neural Networks for DOS Machines", description = "An upcoming and interesting topic in computer science applied in a way that defies reason. You are invited to attend a dazzling, yet dysfunctional, display of DOS's nifty neural networks not working.", event_type = "Colloqiuem", street = "11 Svengard Roundabout",city="Rostok", country="Frisia")
    event_c = models.Event(user = user_c, year = 2016, month = 1, day = 15, title = "Whitehats of the Mediterranean", description = "A practical demonstration of hacking techniques where the audience is expected to take a shot for each intrusion.", event_type = "Colloqiuem", street = "Mustafa Kamal Street",city="Instanbul-Not-Costantinople", country="The Sultanate of Rum") 
	event_a.save()
	event_b.save()
	event_c.save()
	# create some Adverts (x3)
    advert_a = models.Advert(user = user_a,contact_details = "saul-does-not-exist@gmail.com", city = "Ulm", country = "The Kingdom of Bohemia", title = "Help wanted!", description = "We are Junktec. Junktec is looking for Mobile Architects that are ready to architect and build both completely new mobile applications and overhaul legacy mobile applications on both iOS and Android. With your deep experience with the native APIs, you know how to build those showcase apps that have features or visuals (maybe even a little 3d rendering!) that can only be done as an app. You will partner closely with back-end engineers, designers, and product management to ensure features are developed holistically. You should have an unrelenting drive for quality, with a passion for responsive UIs and tight clean animations. Importantly, you will be expected to apply your already deep understanding of the unique characteristics of mobile platforms, both from a frontend and backend perspective, to not only define and implement the key architecture components of the mobile app, but also give recommendations for backend services that can support the user experience desires of product management. ",\
     reference = "Saul/ULM123", closing_date = date(2015,12,31), annual_salary = 500000) 
    advert_b = models.Advert(user = user_b,contact_details = "bob-does-not-exist@gmail.com", city = "Lubeck", country = "Holstein", title = "Assistance needed!", description = '''
Ramazan Development Centre in Cape Town is looking for passionate, experienced software developers to help solve seriously challenging problems in the hyper-opportunity Elastic Compute Cloud (EC2), Ramazan's pioneering cloud computing web service that provides resizable compute capacity in the cloud.

We are continuing to build the EC2 Launch Control team in order to expand on our feature set and manage our rapidly increasing scale. This team is responsible for the development and operation of core services managing the millions of customer resources launched every day in the EC2 cloud.

As an EC2 Launch Control team member you will become part of an industry-leading engineering team solving challenging problems at massive scale and contributing to a wide range of projects in a highly collaborative and fast-paced environment.

You should be:
Clearly passionate about software development, cloud computing and web services in general
Vocal about delivering high quality solutions
Able to thrive in a hyper-growth environment where priorities shift fast

You think about:
Building massively scalable mission-critical systems
Developing algorithms and systems that impact millions of customers, for better or worse
Optimize the performance and stability of highly-available distributed systems
''', reference = "GJD-82", closing_date = date(2016,7,1) , annual_salary = 500000) 
    advert_c = models.Advert(user = user_c,contact_details = "julie-does-not-exist@gmail.com", city = "Verden", country = "Burgundy", title = "Bundles of Bucks", description = "No work ethic required. We are literally giving away money.", reference = "JULIE-KDF", annual_salary = 5000000) 
	advert_a.save()
	advert_b.save()
	advert_c.save()
	# create some Forums
    forum_a = models.Forum(title = "CS Overflow")
    forum_b = models.Forum(title = "World News")
    forum_c = models.Forum(title = "General Discussion")
    #forum_d = models.Forum(title = "Technical Territory")
	forum_a.save()
	forum_b.save()
	forum_c.save()
	#forum_d.save()
	# create some Threads within the above Forums as well as some posts
	# "CS Overflow: A forum for Q and A" Forum:
    thread_a_one = models.Thread(forum = forum_a, creating_user = user_a, title = "Why isn't my code working?")
    thread_a_one.save()
    thread_a_two = models.Thread(forum = forum_a, creating_user = user_c, title = "Jeff Atwood Fan Club")
    thread_a_two.save()

    # World News
    thread_b_one = models.Thread(forum = forum_b, creating_user = user_b, title = "Japan's new diet: Springbok")
    thread_b_one.save()
    post_b_one_one = models.Post(thread = thread_b_one, creating_user = user_b, title = "What a game.", text = "Absolutely 'Rekt'. I'm seriously considering supporting another game.")
    post_b_one_one.save()

    # General Discussion
    thread_c_one = models.Thread(forum = forum_c, creating_user = user_c, title = "Jokes")
    thread_c_one.save()

    post_c_one_one = models.Post(thread = thread_c_one, creating_user = user_c, title = "Here it goes", text = "I went to the CS Alumni Restaurant... ... ... the servers were all busy!")
    post_c_one_one.save()
    

	
