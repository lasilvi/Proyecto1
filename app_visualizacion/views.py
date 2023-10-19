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
from xhtml2pdf import pisa 
from django.urls import reverse
from .forms import *

# Create your views here.
@login_required
def index(request):
    # Obtén el nombre de usuario del objeto request.user
    username = request.user
    
    #todas las actas en las que esta el asistente 
    user = User.objects.get(mail=username)   
    Confirmation_user = Confirmation.objects.filter(user_id = user)
    #actas por aprobar 
    Confirmation_unapproved = Confirmation.objects.filter(Q(user_id = user) & Q(approved=False))
   
    return render(request, 'app_visualizacion/index.html',{'username': username, 'Confirmation_user':Confirmation_user,'Confirmation_unapproved':Confirmation_unapproved})

@login_required
def index2(request):
   # Obtén el nombre de usuario del objeto request.user
    username = request.user
    
    #todas las actas en las que esta el asistente 
    user = User.objects.get(mail=username)   
    Confirmation_user = Confirmation.objects.filter(Q(user_id = user) & Q(approved=True))
   
    return render(request, 'app_visualizacion/index2.html',{'username': username, 'Confirmation_user':Confirmation_user})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request=request, data = request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirige al índice después de iniciar sesión
        else:
            for key, error in list (form.errors.items()):
                messages.error(request, error)
    form =  UserLoginForm()

    return render(request=request, template_name="registration/login.html",context={'form': form})

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
            #todas las actas en las que esta el asistente 
            user = User.objects.get(mail=username)  
            asistente = Confirmation.objects.get(act_id = act_id, user_id = user)
            Aprovar(asistente)
            return redirect('resumen1', act_id=act_id)
        if  action == 'enviar_info':
            username = request.user
            
            comentario = request.POST.get('comentario')
            Enviar_Comentario(act_id,comentario, username)
            return redirect('resumen1', act_id=act_id)
            
    return render(request, 'app_visualizacion/resumen1.html', {'datos': datos_acta,
                                                         'desarrollo': datos_desarrollo,
                                                          'asistentes': asistentes,
                                                         'compromisos': compromisos,'act_id':act_id})

@login_required
def Resumen2(request,act_id):
    # Realiza la consulta y el filtrado de los datos
    datos_acta = Act.objects.filter(pk=act_id)
    datos_desarrollo = Development.objects.filter(act_id=act_id)
    
    asistentes = Confirmation.objects.filter(act_id = act_id)
    compromisos = Commitment.objects.filter(act_id=act_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'generarpdf':
            html_template = 'app_visualizacion/pdf2.html'
            html_string = get_template(html_template).render(
                request=request, context={'datos': datos_acta,
                        'desarrollo': datos_desarrollo,
                        'asistentes': asistentes,
                        'compromisos': compromisos,
                        'act_id':act_id})

            def convert_html_to_pdf(html_string):
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="actadereunión.pdf"'

                # Convierte el HTML en PDF y lo agrega a la respuesta
                pisaStatus = pisa.CreatePDF(html_string, dest=response)

                return response
            # Llama a la función para convertir HTML a PDF
            pdf_response = convert_html_to_pdf(html_string)

            return pdf_response
            

    return render(request, 'app_visualizacion/resumen2.html', {'datos': datos_acta,
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
    