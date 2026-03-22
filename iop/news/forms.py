# Formularz z polami ceny, kategorii oraz zdjęcia
from django import forms
from .models import Articles

class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        # Dodajemy 'image' na koniec listy pól
        fields = ['title', 'excerpt', 'body', 'price', 'category', 'image']
        
        # Polskie nazwy wyświetlane nad okienkami
        labels = {
            'title': 'Tytuł ogłoszenia',
            'excerpt': 'Krótki opis',
            'body': 'Pełny opis',
            'price': 'Cena (zł)',
            'category': 'Kategoria',
            'image': 'Dodaj zdjęcie przedmiotu',
        }
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'excerpt': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
            }),
            # Widget dla zdjęcia, aby wyglądał spójnie z resztą
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }