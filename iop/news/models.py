# Model ogłoszenia z obsługą zdjęć, ceny i kategorii
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Articles(models.Model):
    # Lista kategorii do wyboru w ogłoszeniu
    KATEGORIE = [
        ('elektronika', 'Elektronika'),
        ('dom', 'Dom i Ogród'),
        ('moda', 'Moda'),
        ('motoryzacja', 'Motoryzacja'),
        ('inne', 'Inne'),
    ]

    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Tytuł ogłoszenia', max_length=100, null=False, blank=False)
    excerpt = models.CharField('Krótki opis', max_length=250, null=False, blank=False)
    body = models.TextField('Pełny opis przedmiotu', null=False, blank=True)
    published_at = models.DateTimeField('Data publikacji', auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
        
    price = models.DecimalField(
        'Cena', 
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.0)], 
        default=0.00
    )
    
    category = models.CharField(
        'Kategoria', 
        max_length=50, 
        choices=KATEGORIE, 
        default='inne'
    )

    # NOWE POLE NA ZDJĘCIE:
    # Zdjęcia będą trafiać do folderu 'media/ogloszenia/'
    image = models.ImageField(
        'Zdjęcie przedmiotu', 
        upload_to='ogloszenia/', 
        blank=True, 
        null=True
    )

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = 'Ogłoszenie'
        verbose_name_plural = 'Ogłoszenia'

    def __str__(self):
        return self.title
    
class Ulubione(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ulubione')
    ogloszenie = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='ulubione')
    data_dodania = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ogloszenie')

    def __str__(self):
        return f"{self.user} lubi {self.ogloszenie}"