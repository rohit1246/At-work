from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('work/<str:worktype>/', views.workPage, name='work'),
    path('search/', views.searchPage, name='search'),
    path('profile-settings/', views.settingsPage, name='profile-settings'),
    path('deleteaccount/', views.deleteaccountPage, name='deleteaccount'),
    path('ratings/<str:u>', views.ratingsPage, name='ratings'),
    path('about/',views.about,name='about'),
    path('ourmissions/',views.ourmissions,name='ourmissions'),

]
