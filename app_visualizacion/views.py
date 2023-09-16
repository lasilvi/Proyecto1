from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app_registro.models import *
from django.contrib.auth import authenticate, login, logout
from django.db.models import Max,Q
from django.core.mail import send_mail
from django.contrib.auth.views import LogoutView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

# Create your views here.
@login_required
def index(request):
    # Obtén el nombre de usuario del objeto request.user
    username = request.user
    usermail = username.email

    #todas las actas en las que esta el asistente 
    user = User.objects.get(mail=usermail)   
    Confirmation_user = Confirmation.objects.filter(user_id = user)
    #actas por aprobar 
    Confirmation_unapproved = Confirmation.objects.filter(Q(user_id = user) & Q(approved=False))
   
    return render(request, 'app_visualizacion/index.html',{'username': username, 'Confirmation_user':Confirmation_user,'Confirmation_unapproved':Confirmation_unapproved})

@login_required
def index2(request):
    # Obtén el nombre de usuario del objeto request.user
    username = request.user
    usermail = username.email

    #todas las actas en las que esta el asistente 
    user = User.objects.get(mail=usermail)   
    Confirmation_user = Confirmation.objects.filter(Q(user_id = user) & Q(approved=True))
   
    return render(request, 'app_visualizacion/index2.html',{'username': username, 'Confirmation_user':Confirmation_user})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirige al índice después de iniciar sesión
    return render(request, 'app_visualizacion/login.html')

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Actualiza la sesión del usuario
            return redirect('login')  # Redirige a la página de perfil o a donde desees
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app_visualizacion/contraseña.html', {'form': form})

@login_required
def Resumen1(request,act_id):
    # Realiza la consulta y el filtrado de los datos
    datos_acta = Act.objects.filter(pk=act_id)
    datos_desarrollo = Development.objects.filter(act_id=act_id)
    
    asistentes = Confirmation.objects.filter(act_id = act_id)
    compromisos = Commitment.objects.filter(act_id=act_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'aprobar':
            username = request.user
            usermail = username.email
            #todas las actas en las que esta el asistente 
            user = User.objects.get(mail=usermail)  
            asistente = Confirmation.objects.get(act_id = act_id, user_id = user)
            Aprovar(asistente)
            return redirect('resumen1', act_id=act_id)
        if  action == 'enviar_info':
            username = request.user
            usermail = username.email
            print(usermail)
            comentario = request.POST.get('comentario')
            Enviar_Comentario(act_id,comentario, usermail)
            return redirect('resumen1', act_id=act_id)
        if action == 'generarpdf':
            template = get_template('resumen1')
           
            

    return render(request, 'app_visualizacion/resumen1.html', {'datos': datos_acta,
                                                         'desarrollo': datos_desarrollo,
                                                          'asistentes': asistentes,
                                                         'compromisos': compromisos,'act_id':act_id})

def Aprovar(confirmacion):
    confirmacion.approved = True
    confirmacion.save()

def Enviar_Comentario(act_id, comentario, usuario):
        datos_acta = Act.objects.filter(pk=act_id)
        for dato in datos_acta:
            numero = dato.ident
            proceso = dato.process_text.name
            tipo = dato.type_meet.name
        subject = 'Comentario del Acta'
        message =  'Usuario: ' + usuario +  "\n" +  'comentario: ' + comentario + "\n" +  "Información del acta" + "\n" + "Acta N°: " + str(numero) + "\n" + "Porceso: " + proceso  + "\n" + "Tipo de reunion: " + tipo
        from_email = 'escuelainteramericanadebibliot@gmail.com'
        recipient_list = ['escuelainteramericanadebibliot@gmail.com']

        send_mail(subject, message, from_email,  recipient_list)
        return redirect('resumen1', act_id=act_id)  # Redirigir a la página de filtrado de actas después de guardar los cambios

def sigin_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('username')
        correo = request.POST.get('correo')
        subject = 'Solicitud de registro'
        message =  'Usuario: ' + nombre +  "\n"  + 'correo: ' + correo
        from_email = 'escuelainteramericanadebibliot@gmail.com'
        recipient_list = ['escuelainteramericanadebibliot@gmail.com']

        send_mail(subject, message, from_email,  recipient_list)
        return redirect('sigin')  # Redirige al índice después de iniciar sesión
    return render(request, 'registration/sigin.html')
    