from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', required= True , widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder':"Логин"}))
    password1= forms.CharField(label='Пароль', required= True , widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder':"Пароль"}))
    password2 = forms.CharField(label='Подтверждение пароля', required= True , widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder':"Подтверждение пароля"}))
    email = forms.EmailField(label='Почта', required= True , widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder':"Почта"}))
    first_name = forms.CharField(label='Имя', required= False , widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder':"Имя"}))
    last_name = forms.CharField(label='Логин', required= False , widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder':"Фамилия"}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            return user
