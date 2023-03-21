from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .forms import SignUpForm, DetailsForm, RatingsForm
from django.contrib import messages
from .models import personalInfo, workRatings
from django.db.models import Q
import re
import pandas as pd
import numpy as np
# from pickles import fnames,model,pivot,unames
import pickle
from sklearn.neighbors import NearestNeighbors
from . import pickles
import dill

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check(email):
	if(re.fullmatch(regex, email)):
		return True
	else:
		return False
  
 
def loginPage(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        
        email = request.POST.get('email')
        phoneNumber = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        username = ""

        
        try:
            if check(email):
                email = User.objects.get(email = email)
            else:
                ph_username = personalInfo.objects.all().filter(phoneNumber = phoneNumber)
                for x in ph_username:
                    email = x
            username = User.objects.get(username=email)
            
        except:
            messages.error(request, 'User does not exist')

        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is wrong')

    context = {'page': page}
    return render(request, 'home.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')


def registerPage(request):

    form = SignUpForm()
    userdataform = DetailsForm()
    

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        userdataform = DetailsForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            
            user = form.save()
            info = personalInfo()
            info.email = user
            info.phoneNumber = request.POST.get('phoneNumber')
            info.state = request.POST.get('state')
            info.city = request.POST.get('city').lower()

            workArr = ['electrician', 'plumber', 'painter', 'carrepair', 
            'tutor', 'transport', 'tailor']


            for work in workArr:
                if request.POST.get(work) == 'on':
                    setattr(info, work, True)
                else:
                    setattr(info, work, False)

            info.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred!')
        

    context = {'form':form, 'userdataform':userdataform}
    
    return render(request, 'base/register.html', context)


def ratingsPage(request, u):

    if not request.user.is_authenticated:
        return render(request, 'home.html')

    
    user = request.user
    context = {}
    try:
        ratingsform = workRatings.objects.get(professionalId=u,custoId=user)
        electricianRating = ratingsform.electricianRating
        plumberRating = ratingsform.plumberRating
        painterRating = ratingsform.painterRating
        carrepairRating = ratingsform.carrepairRating
        tailorRating = ratingsform.tailorRating
        transportRating = ratingsform.transportRating
        tutorRating = ratingsform.tutorRating
        context = { 'electricianRating': electricianRating,
                    'plumberRating': plumberRating,
                    'painterRating': painterRating,
                    'carrepairRating': carrepairRating,
                    'tailorRating': tailorRating,
                    'transportRating': transportRating,
                    'tutorRating': tutorRating }
    except:
        print("no ratings")
    
    if request.method == 'POST':
        try:
            print(u)
            ratingsform = workRatings.objects.get(professionalId=u,custoId=user)
            print(ratingsform)
            ratingsform.electricianRating= request.POST.get('electricianRating')
            ratingsform.plumberRating= request.POST.get('plumberRating')
            ratingsform.painterRating= request.POST.get('painterRating')
            ratingsform.carrepairRating= request.POST.get('carrepairRating')
            ratingsform.tailorRating= request.POST.get('tailorRating')
            ratingsform.transportRating= request.POST.get('transportRating')
            ratingsform.tutorRating= request.POST.get('tutorRating')
            ratingsform.save()

            electricianRating = ratingsform.electricianRating
            plumberRating = ratingsform.plumberRating
            painterRating = ratingsform.painterRating
            carrepairRating = ratingsform.carrepairRating
            tailorRating = ratingsform.tailorRating
            transportRating = ratingsform.transportRating
            tutorRating = ratingsform.tutorRating

            context = {'electricianRating':electricianRating,
                    'plumberRating':plumberRating,
                    'painterRating':painterRating,
                    'carrepairRating':carrepairRating,
                    'tailorRating':tailorRating,
                    'transportRating':transportRating,
                    'tutorRating':tutorRating}
        except:
            rate = workRatings()
            rate.professionalId = u
            rate.custoId = user
            print(rate)
            rate.electricianRating= request.POST.get('electricianRating')
            rate.plumberRating= request.POST.get('plumberRating')
            rate.painterRating= request.POST.get('painterRating')
            rate.carrepairRating= request.POST.get('carrepairRating')
            rate.tailorRating= request.POST.get('tailorRating')
            rate.transportRating= request.POST.get('transportRating')
            rate.tutorRating= request.POST.get('tutorRating')
            rate.save()

            electricianRating = rate.electricianRating
            plumberRating = rate.plumberRating
            painterRating = rate.painterRating
            carrepairRating = rate.carrepairRating
            tailorRating = rate.tailorRating
            transportRating = rate.transportRating
            tutorRating = rate.tutorRating
            context = {'electricianRating':electricianRating,
                    'plumberRating':plumberRating,
                    'painterRating':painterRating,
                    'carrepairRating':carrepairRating,
                    'tailorRating':tailorRating,
                    'transportRating':transportRating,
                    'tutorRating':tutorRating,
                    }
        
    return render(request, 'base/ratings.html', context)

def settingsPage(request):
    user = request.user
    userform = SignUpForm(instance = user)
    details = personalInfo.objects.get(email=user)
    
    detailsform = DetailsForm(instance=details)
    pic = personalInfo.objects.filter(email=user)
    

    if request.method == 'POST':
        if request.POST.get("form_type") == 'formOne':
            form = DetailsForm(request.POST, request.FILES, instance=details)

            for field in form:
                print("Field Error: ", field.name,  field.errors)

            if form.is_valid():
                
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                
                user.save()

                details.email = user
                details.phoneNumber = request.POST.get('phoneNumber')
                details.state = request.POST.get('state')
                details.city = request.POST.get('city')
                details.profile_pic = request.FILES.get('profile_pic')

                workArr = ['electrician', 'plumber', 'painter', 'carrepair', 
                'tutot', 'transport', 'tailor']

                for work in workArr:
                    if request.POST.get(work) == 'on':
                        setattr(details, work, True)

                details.save()

                userform = SignUpForm(instance = user)
                detailsform = DetailsForm(instance=details)

            else:
                print("error")
                messages.error(request, 'Something went wrong')

        elif request.POST.get("form_type") == 'formTwo':
            userdataform = SignUpForm(request.POST, instance=user)

            for field in userdataform:
                print( "errors: ", field.errors)

            if userdataform.is_valid():
                print(userdataform)
    
        
    user = User.objects.filter(username = user).all()
    val = []
    for x in user:
        val.append(x)
    user = val
    context = {'userform':userform, 'detailsform': detailsform, 'user':user , 'pic':pic}

    return render(request, 'base/settings.html', context)

def deleteaccountPage(request):

    email = request.POST.get('email')
    phoneNumber = request.POST.get('phoneNumber')
    username = ""

    try:
        if check(email):
            email = User.objects.get(email = email)
        else:
            ph_username = personalInfo.objects.all().filter(phoneNumber = phoneNumber)
            for x in ph_username:
                email = x
        username = User.objects.get(username=email)
    except:
        messages.error(request, 'User does not exist')

    if username == request.user:
        logout(request)
        username = personalInfo.objects.get(email = username)
        username.delete()

        username = User.objects.get(username = username)

        username.delete()
        return redirect('home')
    else:
        messages.error(request, "Enter a valid email")

    return render(request, 'home.html')

def home(request):
    user = request.user
    pic = ""

    if user.is_authenticated:
        pic = personalInfo.objects.filter(email=user)

    context = {'pic':pic, 'user': user}

    return render(request, 'home.html', context)

def searchPage(request):

    worktype = request.POST.get('work')
    given_city = request.POST.get('city-location')
    given_city = given_city.lower()


    if worktype == 'electrician':
        worktype = 'Electricians'
        return electricianWork(request, worktype, given_city)
    elif worktype == 'carrepair':
        worktype = 'Car repair'
        return carrepairWork(request, worktype, given_city)
    elif worktype == 'tailor':
        worktype = 'Tailors'
        return tailorWork(request, worktype, given_city)
    elif worktype == 'transport':
        worktype = 'Transport'
        return transportWork(request, worktype, given_city)
    elif worktype == 'tutor':
        worktype = 'Tutors'
        return tutorWork(request, worktype, given_city)
    elif worktype == 'painter':
        worktype = 'Painters'
        return painterWork(request, worktype, given_city)
    elif worktype == 'plumber':
        worktype = 'Plumbers'
        return plumberWork(request, worktype, given_city)
    
    return render(request, 'home.html')



def recommendation(loggedinuser):
    knnmodel=pickle.load(open('base/pickles/model.pkl','rb'))
    fnames_new = pickle.load(open('base/pickles/fnames.pkl','rb'))
    pivot = pickle.load(open('base/pickles/pivot.pkl','rb'))
    unames_old = dill.load(open('base/pickles/unames.pkl','rb'))
    user = loggedinuser

    query = unames_old[user]
    distances,indices=knnmodel.kneighbors(pivot.iloc[query,:].values.reshape(1,-1),n_neighbors=6)

    li = []
    for i in indices.tolist()[0][1:]:
        li.append(fnames_new[i])

    return li


def workPage(request, worktype):

    if worktype == 'Electricians':
        return electricianWork(request, worktype)
    elif worktype == 'Car repair':
        return carrepairWork(request, worktype)
    elif worktype == 'Tailors':
        return tailorWork(request, worktype)
    elif worktype == 'Transport':
        return transportWork(request, worktype)
    elif worktype == 'Tutors':
        return tutorWork(request, worktype)
    elif worktype == 'Painters':
        return painterWork(request, worktype)
    elif worktype == 'Plumbers':
        return plumberWork(request, worktype)
    
    return render(request, 'home.html')

def plumberWork(request, worktype, given_city=""):
    input_city = False
    if given_city:
        inform = personalInfo.objects.all().filter(plumber = True, city = given_city)
        details = personalInfo.objects.all().filter(plumber = True, city = given_city).values()
    else:
        inform = personalInfo.objects.all().filter(plumber = True)
        details = personalInfo.objects.all().filter(plumber = True).values()
    
    userlist = []
    firstnamelist = []
    citylist = []
    for x in inform:
        user = User.objects.get(username=x)
        if user == request.user:
            userlist.append(None)
            firstnamelist.append(user.first_name)
        else:
            userlist.append(user)
            firstnamelist.append(user.first_name)

    for d in details:
        citylist.append(d['city'])

    newlist = zip(firstnamelist, citylist, userlist)
    
    if newlist == [] and input_city == True:
        newlist = None
        input_city = True
    elif newlist == [] and input_city == False:
        input_city = None
        newlist = True
    
    context = {'worktype': worktype, 'inform': inform, 'firstnamelist':firstnamelist, 'citylist':citylist, 'newlist':newlist, 'input_city':input_city}
    
    return render(request, 'base/work.html', context)

def painterWork(request, worktype, given_city=""):
    input_city = False
    if given_city:
        inform = personalInfo.objects.all().filter(painter = True, city = given_city)
        details = personalInfo.objects.all().filter(painter = True, city = given_city).values()
    else:
        inform = personalInfo.objects.all().filter(painter = True)
        details = personalInfo.objects.all().filter(painter = True).values()

    userlist = []
    firstnamelist = []
    citylist = []
    for x in inform:
        user = User.objects.get(username=x)
        if user == request.user:
            userlist.append(None)
            firstnamelist.append(user.first_name)
        else:
            userlist.append(user)
            firstnamelist.append(user.first_name)

    for d in details:
        citylist.append(d['city'])

    newlist = zip(firstnamelist, citylist, userlist)
    
    if newlist == [] and input_city == True:
        newlist = None
        input_city = True
    elif newlist == [] and input_city == False:
        input_city = None
        newlist = True
    
    context = {'worktype': worktype, 'inform': inform, 'firstnamelist':firstnamelist, 'citylist':citylist, 'newlist':newlist, 'input_city':input_city}
    
    return render(request, 'base/work.html', context)

def tutorWork(request, worktype, given_city=""):
    input_city = False
    if given_city:
        inform = personalInfo.objects.all().filter(tutor = True, city = given_city)
        details = personalInfo.objects.all().filter(tutor = True, city = given_city).values()
    else:
        inform = personalInfo.objects.all().filter(tutor = True)
        details = personalInfo.objects.all().filter(tutor = True).values()

    userlist = []
    firstnamelist = []
    citylist = []
    for x in inform:
        user = User.objects.get(username=x)
        if user == request.user:
            userlist.append(None)
            firstnamelist.append(user.first_name)
        else:
            userlist.append(user)
            firstnamelist.append(user.first_name)

    for d in details:
        citylist.append(d['city'])

    newlist = zip(firstnamelist, citylist, userlist)
    
    if newlist == [] and input_city == True:
        newlist = None
        input_city = True
    elif newlist == [] and input_city == False:
        input_city = None
        newlist = True
    
    context = {'worktype': worktype, 'inform': inform, 'firstnamelist':firstnamelist, 'citylist':citylist, 'newlist':newlist, 'input_city':input_city}
    
    return render(request, 'base/work.html', context)

def transportWork(request, worktype, given_city=""):

    input_city = False
    if given_city:
        inform = personalInfo.objects.all().filter(transport = True, city = given_city)
        details = personalInfo.objects.all().filter(transport = True, city = given_city).values()
    else:
        inform = personalInfo.objects.all().filter(transport = True)
        details = personalInfo.objects.all().filter(transport = True).values()

    userlist = []
    firstnamelist = []
    citylist = []
    for x in inform:
        user = User.objects.get(username=x)
        if user == request.user:
            userlist.append(None)
            firstnamelist.append(user.first_name)
        else:
            userlist.append(user)
            firstnamelist.append(user.first_name)

    for d in details:
        citylist.append(d['city'])

    newlist = zip(firstnamelist, citylist, userlist)
    
    if newlist == [] and input_city == True:
        newlist = None
        input_city = True
    elif newlist == [] and input_city == False:
        input_city = None
        newlist = True
    
    context = {'worktype': worktype, 'inform': inform, 'firstnamelist':firstnamelist, 'citylist':citylist, 'newlist':newlist, 'input_city':input_city}
    
    return render(request, 'base/work.html', context)

def tailorWork(request, worktype, given_city=""):

    input_city = False
    if given_city:
        inform = personalInfo.objects.all().filter(tailor = True, city = given_city)
        details = personalInfo.objects.all().filter(tailor = True, city = given_city).values()
    else:
        inform = personalInfo.objects.all().filter(tailor = True)
        details = personalInfo.objects.all().filter(tailor = True).values()


    userlist = []
    firstnamelist = []
    citylist = []
    for x in inform:
        user = User.objects.get(username=x)
        if user == request.user:
            userlist.append(None)
            firstnamelist.append(user.first_name)
        else:
            userlist.append(user)
            firstnamelist.append(user.first_name)

    for d in details:
        citylist.append(d['city'])

    newlist = zip(firstnamelist, citylist, userlist)
    
    if newlist == [] and input_city == True:
        newlist = None
        input_city = True
    elif newlist == [] and input_city == False:
        input_city = None
        newlist = True
    
    context = {'worktype': worktype, 'inform': inform, 'firstnamelist':firstnamelist, 'citylist':citylist, 'newlist':newlist, 'input_city':input_city}
    
    return render(request, 'base/work.html', context)

def carrepairWork(request, worktype, given_city=""):
    input_city = False

    if given_city:
        inform = personalInfo.objects.all().filter(carrepair = True, city = given_city)
        details = personalInfo.objects.all().filter(carrepair = True, city = given_city).values()
    else:
        inform = personalInfo.objects.all().filter(carrepair = True)
        details = personalInfo.objects.all().filter(carrepair = True).values()

    userlist = []
    firstnamelist = []
    citylist = []
    for x in inform:
        user = User.objects.get(username=x)
        if user == request.user:
            userlist.append(None)
            firstnamelist.append(user.first_name)
        else:
            userlist.append(user)
            firstnamelist.append(user.first_name)

    for d in details:
        citylist.append(d['city'])

    newlist = zip(firstnamelist, citylist, userlist)
    
    if newlist == [] and input_city == True:
        newlist = None
        input_city = True
    elif newlist == [] and input_city == False:
        input_city = None
        newlist = True
    
    context = {'worktype': worktype, 'inform': inform, 'firstnamelist':firstnamelist, 'citylist':citylist, 'newlist':newlist, 'input_city':input_city}
    
    return render(request, 'base/work.html', context)

def electricianWork(request, worktype, given_city=""):
    input_city = False

    if given_city:        
        inform = personalInfo.objects.all().filter(electrician = True, city = given_city)
        details = personalInfo.objects.all().filter(electrician = True, city = given_city).values()
        input_city = True
    else:
        inform = personalInfo.objects.all().filter(electrician = True)
        details = personalInfo.objects.all().filter(electrician = True).values()

    userlist = []
    firstnamelist = []
    citylist = []
    for x in inform:
        user = User.objects.get(username=x)
        if user == request.user:
            userlist.append(None)
            firstnamelist.append(user.first_name)
        else:
            userlist.append(user)
            firstnamelist.append(user.first_name)

    for d in details:
        citylist.append(d['city'])

    newlist = zip(firstnamelist, citylist, userlist)
    
    if newlist == [] and input_city == True:
        newlist = None
        input_city = True
    elif newlist == [] and input_city == False:
        input_city = None
        newlist = True
    
    context = {'worktype': worktype, 'inform': inform, 'firstnamelist':firstnamelist, 'citylist':citylist, 'newlist':newlist, 'input_city':input_city}
    
    return render(request, 'base/work.html', context)

def electricianWork(request, worktype, given_city=""):
    input_city = False

    if given_city:        
        inform = personalInfo.objects.all().filter(electrician = True, city = given_city)
        details = personalInfo.objects.all().filter(electrician = True, city = given_city).values()
        input_city = True
    else:
        inform = personalInfo.objects.all().filter(electrician = True)
        details = personalInfo.objects.all().filter(electrician = True).values()

    
    userlist = []
    firstnamelist = []
    citylist = []
    for x in inform:
        user = User.objects.get(username=x)
        if user == request.user :
            userlist.append(None)
            firstnamelist.append(user.first_name)
        else:
            userlist.append(user)
            firstnamelist.append(user.first_name)

    for d in details:
        citylist.append(d['city'])

    newuserlist = []
    newfirstnamelist = []
    newcitylist = []
    user_str_list = [str(user) for user in userlist]
    userlist = user_str_list

    if request.user.is_authenticated:
        userval = str(request.user)
        li = recommendation(userval)
    else:
        li = userlist
        

    
    checkUser = str(request.user)
    
    for u in li:
        if u is not checkUser:
            try:
                idx = userlist.index(u)
                print(idx)
                newuserlist.append(u)
                newfirstnamelist.append(firstnamelist[idx])
                newcitylist.append(citylist[idx])
            except:
                print("user")
    

    newlist = zip(newfirstnamelist, newcitylist, newuserlist)
    
    if newlist == [] and input_city == True:
        newlist = None
        input_city = True
    elif newlist == [] and input_city == False:
        input_city = None
        newlist = True
    
    context = {'worktype': worktype, 'inform': inform, 'firstnamelist':firstnamelist, 'citylist':citylist, 'newlist':newlist, 'input_city':input_city}

    if request.user.is_authenticated:
        ML = "Machine Learning Based top 5 search results"
        context.update(ML=ML)
    
    return render(request, 'base/work.html', context)

def about(request):
    return render(request,"about.html")

def ourmissions(request):
    return render(request,"ourmissions.html")