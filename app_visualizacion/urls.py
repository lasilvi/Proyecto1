"""Importe de las libreraís necesarias."""
from django.urls import path, re_path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('index.html', views.index, name='index'),
    path('index2.html/', views.index2, name='index2'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('resumen1/<int:act_id>/', views.Resumen1, name='resumen1'),
    path('EnviarComentario/<int:act_id>/', views.Enviar_Comentario, name='EnviarComentario'),
    ]