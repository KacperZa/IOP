from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='chat_inbox'),
    path('<int:conv_id>/', views.conversation, name='chat_conversation'),
    path('<int:conv_id>/send/', views.send_message, name='chat_send'),
    path('<int:conv_id>/poll/', views.get_messages, name='chat_poll'),
    path('start/<int:article_id>/', views.start_conversation, name='chat_start'),
    path('<int:conv_id>/delete/', views.delete_conversation, name='chat_delete'),
]