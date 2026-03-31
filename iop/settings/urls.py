from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.settings, name='settings'),
    path('settings/username/', views.change_username, name='change_username'),
    path('settings/password/', views.change_password, name='change_password'),
    path('settings/delete/', views.delete_account, name='delete_account'),
    path('settings/avatar/', views.change_avatar, name='change_avatar'),
]