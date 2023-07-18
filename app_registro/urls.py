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
    path('RegistroAsistente/', views.RegisterAssistant, name='RegisterAssistant'),
    path('edit_act/<int:act_id>/', views.edit_act, name='edit_act'),
    path('filter-acts/', views.filter_acts, name='filter_acts'),
    path('EditarUsuario/<int:user_id>/', views.editar_usuario, name='EditarUsuario'),
    path('eliminar_usuario/', views.eliminar_usuario, name='eliminar_usuario'),
    path('RegistroProceso', views.RegisterProcess, name='RegisterProcess'),
    path('EditarProceso/<int:process_id>/', views.editar_Proceso, name='EditarProceso'),
    path('RegistroTipodeReunion/', views.RegisterTypemeet, name='RegisterTypemeet'),
     path('EditarTipodeReunion/<int:tmeet_id>/', views.editar_Tipodereunion, name='EditarTipoReunion'),
    ]