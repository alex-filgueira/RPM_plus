from django import forms

from django.core.exceptions import ValidationError
#from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.

#Aquí defino enteramente un formulario


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

#Custom form for register user
class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user

"""
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

# Aquí utilizo un modelo
from django.forms import ModelForm
from .models import *

class RenewBookModelForm(ModelForm):
    def clean_name(self):
       data = self.cleaned_data['name']
       #print(data)

       #Check date is not in past.
       if len(data) < 1:
           raise ValidationError(_('Invalid date - Empty'))

       # Remember to always return the cleaned data.
       return data

    class Meta:
        model = MProject
        fields = ['name',]
        labels = { 'name': _('Renewal name'), }
        help_texts = { 'name': _('Enter a date between now and 4 weeks (default 3).'), } 
"""
