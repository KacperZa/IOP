# Plik do zarządzania ścieżkami w aplikacji. Zawiera listę ścieżek powiązanych z widokami.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('cars', views.article, name='cars'),
    path('contact', views.contact, name='contact'),
    path('login', views.login_user, name='login_user'),
    path('register', views.register, name='register_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('ogloszenie/<int:ogloszenie_id>/ulubione/', views.toggle_ulubione, name='toggle_ulubione'),

]
