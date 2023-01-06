from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-xl','placeholder':"Username "}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-xl','placeholder':"Password "}))

class RegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-xl','placeholder':"Email "}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-xl','placeholder':"Password "}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-xl','placeholder':"Name "}))
    department = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-xl','placeholder':"Department "}))
    contact = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-xl','placeholder':"Contact "}))