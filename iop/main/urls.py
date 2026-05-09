# Plik do zarządzania ścieżkami w aplikacji. Zawiera listę ścieżek powiązanych z widokami.

from django.urls import path
from . import views
from news.views import NewsDetailView, NewsUpdateView, NewsDeleteView
from django.conf.urls import include

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('cars', views.article, name='cars'),
    path('contact', views.contact, name='contact'),
    path('login', views.login_user, name='login_user'),
    path('register', views.register, name='register_user'),
    path('logout', views.logout_user, name='logout_user'),    
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('news/<int:pk>/update/', NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('ogloszenie/<int:ogloszenie_id>/ulubione/', views.toggle_ulubione, name='toggle_ulubione'),
    path('settings/', include('settings.urls')),
    path('regulamin', views.regulamin, name='regulamin'),
    path('favourites', views.favourites, name='favourites'),

]



    


    