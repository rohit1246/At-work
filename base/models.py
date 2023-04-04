from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint


class personalInfo(models.Model):
    phoneNumber = models.CharField(max_length=20, unique=True, null=True, blank = False)
    email = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, unique=True)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    profile_pic = models.ImageField(null=True, default='man.png')

    electrician = models.BooleanField(null=True)
    plumber = models.BooleanField(null=True)
    painter = models.BooleanField(null=True)
    carrepair = models.BooleanField(null=True)
    tailor = models.BooleanField(null=True)
    transport = models.BooleanField(null=True)
    tutor = models.BooleanField(null=True)
    
    def __str__(self):
        return str(self.email)

class workRatings(models.Model):
    id = models.IntegerField(primary_key=True)
    professionalId = models.CharField(max_length=100)
    custoId = models.CharField(max_length=100, default=User)

    electricianRating = models.CharField(max_length=20, null=True, blank = False)
    plumberRating = models.CharField(max_length=20, null=True, blank = False)
    painterRating = models.CharField(max_length=20, null=True, blank = False)
    carrepairRating = models.CharField(max_length=20, null=True, blank = False)
    tailorRating = models.CharField(max_length=20, null=True, blank = False)
    transportRating = models.CharField(max_length=20, null=True, blank = False)
    tutorRating = models.CharField(max_length=20, null=True, blank = False)

    def __str__(self):
        return str(self.custoId)

