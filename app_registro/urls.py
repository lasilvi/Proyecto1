"""Importe de las libreraís necesarias."""
from django.urls import path, re_path
from . import views
from .views import MenuView

urlpatterns = [
    path('menu/', MenuView.as_view(), name='menu'),
    path('RegistroActa/', views.Register, name='Registro'),
    path('RegistroUsuariosConfirmacion/', views.RegisterUserConfirmation, name='RegistroUserconfirmation'),
    path('RegistroDesarrollo/', views.RegisterDevelopment, name='RegistroDevelop'),
    path('RegistroCompromiso/', views.RegisterCommintment, name='RegistroCommintment'),
    path('resumen/', views.Summary, name='resumen'),
    ]