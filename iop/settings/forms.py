from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta: 
        model = Profile
        fields = ['gender', 'age']
    
class AvatarForm(forms.Form):
    avatar = forms.ImageField()