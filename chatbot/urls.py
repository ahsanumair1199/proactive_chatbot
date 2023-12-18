from django.urls import path
from . import views

urlpatterns = [
    path('message/', views.whatsapp_user_response,
         name='whatsapp_user_response'),
]
