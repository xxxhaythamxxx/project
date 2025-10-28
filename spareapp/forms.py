from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    # email = forms.EmailField()
    username = forms.CharField(label="Username",widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.CharField(label="Email",widget=forms.TextInput(attrs={'class': "form-control"}))
    # password1 = forms.CharField(label="Password",widget=forms.PasswordInput)
    # password2 = forms.CharField(label="Confirm password",widget=forms.PasswordInput)

    # email = forms.EmailField(label="Email",widget=forms.TextInput(attrs={'class': "form-control"}))
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class': "form-control"}))
    password2 = forms.CharField(label="Confirm password",widget=forms.PasswordInput(attrs={'class': "form-control"}))
    
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        help_texts = {k:"" for k in fields }

class UploadExcelForm(forms.Form):
    archivo = forms.FileField(label="Selecciona un archivo Excel (.xlsx)")