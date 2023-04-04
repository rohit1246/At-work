from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import personalInfo, workRatings
from PIL import Image
 
class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'username', 
            'id':'username', 
            'type':'text', 
            'placeholder':'e.g. John_Doe', 
            'maxlength': '16', 
            'minlength': '6', 
            })
        self.fields['email'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'email', 
            'id':'email', 
            'type':'email', 
            'placeholder':'e.g. JohnDoe@mail.com', 
            }) 
        self.fields['password1'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'password1', 
            'id':'password1', 
            'type':'password', 
            'placeholder':'password', 
            'maxlength':'22',  
            'minlength':'8' 
            }) 
        self.fields['password2'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'password2', 
            'id':'password2', 
            'type':'password', 
            'placeholder':'password', 
            'maxlength':'22',  
            'minlength':'8' 
            })
        self.fields['first_name'].widget.attrs.update({ 
            'class': 'form-input',
            'required':'', 
            'name':'first_name', 
            'id':'', 
            'type':'text', 
            'placeholder':'e.g. John', 
            'maxlength':'50',
            'minlength':'1' 
            })
        self.fields['last_name'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'False', 
            'name':'Doe', 
            'id':'', 
            'type':'text', 
            'placeholder':'e.g. Doe', 
            'maxlength':'50',
            'minlength':'1' 
            })
        
 
    username = forms.CharField(max_length = 20, label = False)
    email = forms.EmailField(max_length = 100)

    first_name = forms.CharField(max_length = 50, label = False)
    last_name = forms.CharField(max_length = 50, label = False)

    class Meta:
        model = User
        fields = (
        'username', 'email', 'password1',
        'password2', 'first_name', 'last_name'
        )




class DetailsForm(ModelForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.fields['phoneNumber'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'phoneNumber', 
            'id':'phoneNumber', 
            'type':'text', 
            'placeholder':'e.g. 9856237845', 
            'maxlength': '16', 
            'minlength': '6',
            }) 
        self.fields['state'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'state', 
            'id':'', 
            'type':'text', 
            'placeholder':'e.g. Florida', 
            'maxlength':'50',
            'minlength':'1' 
            })
        self.fields['city'].widget.attrs.update({ 
            'class': 'form-input', 
            'required':'', 
            'name':'city', 
            'id':'', 
            'type':'text', 
            'placeholder':'e.g. Miami',
            'maxlength':'50',
            'minlength':'1' 
            })
        
        
            
        
 
    phoneNumber = forms.CharField(max_length = 20, label = False)
    state = forms.CharField(max_length = 20, label = False)
    city = forms.CharField(max_length = 20, label = False)
    # profile_pic = forms.ImageField()


    electrician = forms.BooleanField(required=False)
    painter = forms.BooleanField(required=False)
    plumber = forms.BooleanField(required=False)

    tailor = forms.BooleanField(required=False)
    transport = forms.BooleanField(required=False)
    tutor = forms.BooleanField(required=False)
    carrepair = forms.BooleanField(required=False)   
 
    class Meta:
        model = personalInfo
        # , 'profile_pic'
        fields = (
        'phoneNumber', 'state', 'city'
        , 'carrepair', 'painter', 'electrician', 'tutor'
        , 'transport', 'tailor', 'plumber',
        )



class RatingsForm(ModelForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.fields['professionalId'].widget.attrs.update({ 
            'class': '', 
            'required':'', 
            'name':'professionalId', 
            'id':'', 
            'type':'text', 
            'placeholder':'', 
            'maxlength':'50',
            'minlength':'1' 
            })
        self.fields['customerId'].widget.attrs.update({ 
            'class': '', 
            'required':'', 
            'name':'customerId', 
            'id':'', 
            'type':'text', 
            'placeholder':'',
            'maxlength':'50',
            'minlength':'1' 
            })
    
    professionalId = forms.CharField(max_length = 20, label = False)
    customerId = forms.CharField(max_length = 20, label = False)
    


    electricianRating = forms.IntegerField(required=False)
    painterRating = forms.IntegerField(required=False)
    plumberRating = forms.IntegerField(required=False)

    tailorRating = forms.IntegerField(required=False)
    transportRating = forms.IntegerField(required=False)
    tutorRating = forms.IntegerField(required=False)
    carrepairRating = forms.IntegerField(required=False)   
 
    class Meta:
        model = workRatings
        fields = (
        'professionalId', 'customerId'
        , 'carrepairRating', 'painterRating', 'electricianRating','tutorRating'
        , 'transportRating', 'tailorRating', 'plumberRating',
        )