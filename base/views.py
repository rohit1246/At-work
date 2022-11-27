from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .forms import SignUpForm, DetailsForm
from django.contrib import messages
from .models import personalInfo
from django.db.models import Q
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check(email):
	if(re.fullmatch(regex, email)):
		return True
	else:
		return False
  
 
def loginPage(request):
    page= 'login'
    
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        
        email = request.POST.get('email')
        phoneNumber = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        username = ""

        
        try:
            print("before ", email)
            if check(email):
                print("entered email") 
                email = User.objects.get(email = email)
            else:
                print("entered ph")
                ph_username = personalInfo.objects.all().filter(phoneNumber = phoneNumber)
                for x in ph_username:
                    email = x

            print("after ",email)
            
            username = User.objects.get(username=email)
            
        except:
            messages.error(request, 'User does not exist')

        print("username ",username)
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is wrong')

    context = {'page':page}
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

            print(request.POST)
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

def settingsPage(request):
    user = request.user
    userform = SignUpForm(instance = user)
    details = personalInfo.objects.get(email=user)
    detailsform = DetailsForm(instance=details)
    pic = personalInfo.objects.filter(email=user)
    

    if request.method == 'POST':
        if request.POST.get("form_type") == 'formOne':
            form = DetailsForm(request.POST, request.FILES, instance=details)

            print(request.POST)
            print(form.is_valid())

            for field in form:
                print("Field Error: ", field.name,  field.errors)

            if form.is_valid():
                
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                
                user.save()
                print(user)


                details.email = user
                details.phoneNumber = request.POST.get('phoneNumber')
                details.state = request.POST.get('state')
                details.city = request.POST.get('city')
                details.profile_pic = request.FILES.get('profile_pic')
                print(details.profile_pic)
                print(request.FILES.get('profile_pic'))

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
            print(userdataform)

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
        print("before ", email)
        if check(email):
            print("entered email") 
            email = User.objects.get(email = email)
        else:
            print("entered ph")
            ph_username = personalInfo.objects.all().filter(phoneNumber = phoneNumber)
            for x in ph_username:
                email = x

        print("after ",email)
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

    print(request.POST)

    worktype = request.POST.get('work')
    given_city = request.POST.get('city-location')
    given_city = given_city.lower()
    print(worktype)
    print(given_city)


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

    if given_city:
        inform = personalInfo.objects.all().filter(plumber = True, city = given_city)
        details = personalInfo.objects.all().filter(plumber = True, city = given_city).values()
    else:
        inform = personalInfo.objects.all().filter(plumber = True)
        details = personalInfo.objects.all().filter(plumber = True).values()
    
    userlist = []
    citylist = []
    for x in inform:
        user = User.objects.get(username=x)
        userlist.append(user.first_name)

    for d in details:
        citylist.append(d['city'])


    print(userlist)
    print(citylist)
    newlist = zip(userlist, citylist)
    print(newlist)

    if userlist == [] and citylist == []:
        newlist = False

    print(newlist)

    
    context = {'worktype': worktype, 'inform': inform, 'userlist':userlist, 'citylist':citylist, 'newlist':newlist}
    return render(request, 'base/work.html', context)

def painterWork(request, worktype, given_city=""):

    if given_city:
        inform = personalInfo.objects.all().filter(painter = True, city = given_city)
        details = personalInfo.objects.all().filter(painter = True, city = given_city).values()
    else:
        inform = personalInfo.objects.all().filter(painter = True)
        details = personalInfo.objects.all().filter(painter = True).values()
    print(details)
    print(inform)

    userlist = []
    citylist = []
    for x in inform:
        user = User.objects.get(username=x)
        userlist.append(user.first_name)



    for d in details:
        citylist.append(d['city'])

    print(userlist)
    print(citylist)
    newlist = zip(userlist, citylist)
    print(newlist)

    
    context = {'worktype': worktype, 'inform': inform, 'userlist':userlist, 'citylist':citylist, 'newlist':newlist}
    return render(request, 'base/work.html', context)

def tutorWork(request, worktype, given_city=""):


    if given_city:
        inform = personalInfo.objects.all().filter(tutor = True, city = given_city)
        details = personalInfo.objects.all().filter(tutor = True, city = given_city).values()
    else:
        inform = personalInfo.objects.all().filter(tutor = True)
        details = personalInfo.objects.all().filter(tutor = True).values()
    print(details)
    print(inform)

    userlist = []
    citylist = []
    for x in inform:
        user = User.objects.get(username=x)
        # print(user)
        userlist.append(user.first_name)



    for d in details:
        citylist.append(d['city'])

    print(userlist)
    print(citylist)
    newlist = zip(userlist, citylist)
    print(newlist)

    
    context = {'worktype': worktype, 'inform': inform, 'userlist':userlist, 'citylist':citylist, 'newlist':newlist}
    # context = worktype
    return render(request, 'base/work.html', context)

def transportWork(request, worktype, given_city=""):


    if given_city:
        inform = personalInfo.objects.all().filter(transport = True, city = given_city)
        details = personalInfo.objects.all().filter(transport = True, city = given_city).values()
    else:
        inform = personalInfo.objects.all().filter(transport = True)
        details = personalInfo.objects.all().filter(transport = True).values()
    print(details)
    print(inform)

    userlist = []
    citylist = []
    for x in inform:
        user = User.objects.get(username=x)
        # print(user)
        userlist.append(user.first_name)



    for d in details:
        citylist.append(d['city'])

    print(userlist)
    print(citylist)
    newlist = zip(userlist, citylist)
    print(newlist)

    
    context = {'worktype': worktype, 'inform': inform, 'userlist':userlist, 'citylist':citylist, 'newlist':newlist}
    # context = worktype
    return render(request, 'base/work.html', context)

def tailorWork(request, worktype, given_city=""):


    if given_city:
        inform = personalInfo.objects.all().filter(tailor = True, city = given_city)
        details = personalInfo.objects.all().filter(tailor = True, city = given_city).values()
    else:
        inform = personalInfo.objects.all().filter(tailor = True)
        details = personalInfo.objects.all().filter(tailor = True).values()
    print(details)
    print(inform)

    userlist = []
    citylist = []
    for x in inform:
        user = User.objects.get(username=x)
        # print(user)
        userlist.append(user.first_name)



    for d in details:
        citylist.append(d['city'])

    print(userlist)
    print(citylist)
    newlist = zip(userlist, citylist)
    print(newlist)

    
    context = {'worktype': worktype, 'inform': inform, 'userlist':userlist, 'citylist':citylist, 'newlist':newlist}
    # context = worktype
    return render(request, 'base/work.html', context)

def carrepairWork(request, worktype, given_city=""):


    if given_city:
        inform = personalInfo.objects.all().filter(carrepair = True, city = given_city)
        details = personalInfo.objects.all().filter(carrepair = True, city = given_city).values()
    else:
        inform = personalInfo.objects.all().filter(carrepair = True)
        details = personalInfo.objects.all().filter(carrepair = True).values()
    print(details)
    print(inform)

    userlist = []
    citylist = []
    for x in inform:
        user = User.objects.get(username=x)
        # print(user)
        userlist.append(user.first_name)



    for d in details:
        citylist.append(d['city'])

    print(userlist)
    print(citylist)
    newlist = zip(userlist, citylist)
    print(newlist)

    
    context = {'worktype': worktype, 'inform': inform, 'userlist':userlist, 'citylist':citylist, 'newlist':newlist}
    # context = worktype
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
    print(details)
    print(inform)

    userlist = []
    citylist = []
    for x in inform:
        user = User.objects.get(username=x)
        # print(user)
        userlist.append(user.first_name)



    for d in details:
        citylist.append(d['city'])

    print(userlist)
    print(citylist)
    newlist = zip(userlist, citylist)
    print(newlist)

    if newlist == [] and input_city == True:
        newlist = None
        input_city = True
    elif newlist == [] and input_city == False:
        input_city = None
        newlist = True
    
    context = {'worktype': worktype, 'inform': inform, 'userlist':userlist, 'citylist':citylist, 'newlist':newlist, 'input_city':input_city}
    # context = worktype
    return render(request, 'base/work.html', context)
















# inform = []
     
    # inform = personalInfo.objects.all().filter('worktype' = True)
    # inform = personalInfo.objects.all().filter(electrician = True)
    # details = personalInfo.objects.all().filter(electrician = True).values()
    # print(details)
    # print(inform)

    # userlist = []
    # citylist = []
    # for x in inform:
    #     user = User.objects.get(username=x)
    #     # print(user)
    #     userlist.append(user.first_name)



    # for d in details:
    #     citylist.append(d['city'])

    # print(userlist)
    # print(citylist)
    # newlist = zip(userlist, citylist)
    # print(newlist)

    
    # context = {'worktype': worktype, 'inform': inform, 'userlist':userlist, 'citylist':citylist, 'newlist':newlist}
    # # context = worktype
    # return render(request, 'base/work.html', context)





# def createUser(request):
#     print(request.POST)


#     if request.method == 'POST':
#         # user = form.save(commit = False)

#         user = User.objects.create_user(
#             email = request.POST.get('email'),
#             first_name = request.POST.get('first_name'),
#             last_name = request.POST.get('last_name'),
#             password = request.POST.get('password'),
#             phoneNumber = request.POST.get('phoneNumber'),
#             state = request.POST.get('state'),
#             city = request.POST.get('city'),
#             zipcode = request.POST.get('zipcode'),
#             work = request.POST.get('work')
#             )

#         user.save()
        
        
#         # login(request, user)
#         return redirect('home')

#     return render(request, 'register.html')



# def loginPage(request):
#     page= 'login'
    
#     if request.user.is_authenticated:
#         return redirect('home')

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         try:
#             user = User.objects.get(username=username)
#         except:
#             messages.error(request, 'User does not exist')
        
#         user = authenticate(request, username=username, password = password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Username or password is wrong')

#     context = {'page':page}
#     return render(request, 'base/login_registration.html', context)

# def logoutPage(request):
#     logout(request)
#     return redirect('home')


# def registerPage(request):

#     form = UserCreationForm()

#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit = False)
#             user.username = user.username.lower()
#             user.save()
#             login(request, user)
#             return redirect('home')
#         else: 
#             messages.error(request, 'Something went wrong')

#     context = {'form':form}
#     return render(request, 'base/login_registration.html', context)