from django.contrib.auth.models import User
from .models import personalInfo



def workPage():
    # inform = []
     
    # inform = personalInfo.objects.all().filter('worktype' = True)
    inform = personalInfo.objects.all().filter(electrician = True)
    # print(worktype)
    print(inform)
    userlist = []




    for x in inform:
        user = User.objects.get(username=x)
        userlist.append(user.first_name)
    print(userlist)

    # context = worktype

workPage()






# class work():
#     electrician = False
#     plumber = False
#     painter = False


# w = work()
# arr = ['electrician', 'plumber', 'painter']


# for wk in arr:
#     setattr(w, wk, True)
#     print(getattr(w, wk))
#     if getattr(w, wk) == True :
#         print('ok')
#     else:
#         print("no")
#     # print(w['wk'])
#     # print(w.electrician)

# [a for a in dir(w) if not a.startswith('__') and not callable(getattr(w, a))]
