"""Importe de las libreraís necesarias."""
from django.urls import path, re_path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('resumen1/<int:act_id>/', views.Resumen1, name='resumen1'),
    path('EnviarComentario/<int:act_id>/', views.Enviar_Comentario, name='EnviarComentario'),
    ]