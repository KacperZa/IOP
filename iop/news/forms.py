from django import forms
from .models import Articles

class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'excerpt', 'body', 'price', 'category', 'image']
        
        labels = {
            'title': 'Tytuł ogłoszenia',
            'excerpt': 'Krótki opis',
            'body': 'Pełny opis',
            'price': 'Cena (zł)',
            'category': 'Kategoria',
            'image': 'Dodaj zdjęcie przedmiotu',
        }
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Wpisz tytuł ogłoszenia...'
            }),
            'excerpt': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Krótki opis przedmiotu...'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-textarea', 
                'rows': 4, 
                'placeholder': 'Podaj szczegóły oferty...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'image': forms.FileInput(attrs={'id': 'id_image'}),
        }