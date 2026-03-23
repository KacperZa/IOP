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
<<<<<<< HEAD
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
=======
        verbose_name = 'Ogłoszenie'
        verbose_name_plural = 'Ogłoszenia'

    def __str__(self):
        return self.title
>>>>>>> 4d969f5df22628a66df89df871fc2d28fe640761
