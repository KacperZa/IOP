from django import forms
from .models import Profile
import re
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta: 
        model = Profile
        fields = ['avatar_url']
    
class AvatarForm(forms.Form):
    avatar = forms.ImageField()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Potwierdź hasło')
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control discord-input', 'placeholder':''})
    )

    class Meta: 
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control discord-input', 'placeholder':''})
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$', password):
            raise forms.ValidationError(
                "Hasło musi mieć min. 8 znaków, jedną wielką literę, jedną małą literę i cyfrę."
            )
        return password
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}$', email):
            raise forms.ValidationError(
                "Podaj prawidłowy adres email, np. jan@gmail.com."
            )
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            raise forms.ValidationError('Hasła nie są identyczne')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit: 
            user.save()
        return user