"""Importe de las libreraís necesarias."""
from django.urls import path, re_path
from . import views
from .views import MenuView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('menu/', views.MenuView, name='menu'),
    path('RegistroActa/', views.Register, name='Registro'),
    path('login/', views.login_view1, name='login1'),
    path('logout/', views.logout_view, name='logout1'),
    path('change_password/', views.change_password, name='change_password1'),

    path('RegistroUsuariosConfirmacion/<int:act_id>/<str:act_proceso>/<int:act_ident>/', views.RegisterUserConfirmation, name='RegistroUserconfirmation'),
    path('EditarRegistroUsuariosConfirmacion/<int:user_id>/<int:act_id>/<str:act_proceso>/<int:act_ident>/', views.editar_RegisterUserConfirmation, name='EditarRegistroUsuariosConfirmacion'),
    path('eliminar_RegistroUsuariosConfirmacion/<int:user_id>/<int:act_id>/<str:act_proceso>/<int:act_ident>/', views.eliminar_RegisterUserConfirmation, name='eliminar_RegistroUsuariosConfirmacion'),
    
    path('RegistroDesarrollo/<int:act_id>/<str:act_proceso>/<int:act_ident>/', views.RegisterDevelopment, name='RegistroDevelop'),
    path('EditarRegistroDesarrollo/<int:desarrollo_id>/<int:act_id>/<str:act_proceso>/<int:act_ident>/', views.editar_RegisterDevelopment, name='EditarRegistroDesarrollo'),
    path('eliminar_Desarrollo/<int:desarrollo_id>/<int:act_id>/<str:act_proceso>/<int:act_ident>/', views.eliminar_RegisterDevelopment, name='eliminar_Desarrollo'),

    path('RegistroCompromiso/<int:act_id>/<str:act_proceso>/<int:act_ident>/', views.RegisterCommintment, name='RegistroCommintment'),
    path('EditarRegistroCompromiso/<int:compromiso_id>/<int:act_id>/<str:act_proceso>/<int:act_ident>/', views.editar_RegisterCommintment, name='EditarRegistroCompromiso'),
    path('eliminar_Compromiso/<int:compromiso_id>/<int:act_id>/<str:act_proceso>/<int:act_ident>/', views.eliminar_RegisterCommintment, name='eliminar_Compromiso'),
    
    path('resumen/<int:act_id>/', views.Summary, name='resumen'),
    path('enviar_correo/', views.enviar_correo, name='enviar_correo'),
   
    path('edit_act/<int:act_id>/', views.edit_act, name='edit_act'),
    path('filtrar/', views.filter_acts, name='filter_acts'),
    
    path('RegistroAsistente/', views.RegisterAssistant, name='RegisterAssistant'),
    path('EditarUsuario/<int:user_id>/', views.editar_usuario, name='EditarUsuario'),
    path('eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    path('RegistroProceso', views.RegisterProcess, name='RegisterProcess'),
    path('EditarProceso/<int:process_id>/', views.editar_Proceso, name='EditarProceso'),
    path('eliminar_proceso/<int:dependece_id>/', views.eliminar_proceso, name='eliminar_proceso'),

    path('RegistroTipodeReunion/', views.RegisterTypemeet, name='RegisterTypemeet'),
    path('EditarTipodeReunion/<int:tmeet_id>/', views.editar_Tipodereunion, name='EditarTipoReunion'),
    path('eliminar_tipo_reunion/<int:type_id>/', views.eliminar_tipo_reunion, name='eliminar_tipo_reunion'),
   
    ]