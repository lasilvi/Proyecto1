from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app_registro.models import *
from django.contrib.auth import authenticate, login
from django.db.models import Max,Q
from django.core.mail import send_mail
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

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirige al índice después de iniciar sesión
    return render(request, 'app_visualizacion/login.html')

def Resumen1(request,act_id):
    # Realiza la consulta y el filtrado de los datos
    datos_acta = Act.objects.filter(pk=act_id)
    datos_desarrollo = Development.objects.filter(act_id=act_id)
    
    asistentes = Confirmation.objects.filter(act_id = act_id)
    compromisos = Commitment.objects.filter(act_id=act_id)

    if request.method == 'POST':
        username = request.user
        usermail = username.email
        #todas las actas en las que esta el asistente 
        user = User.objects.get(mail=usermail)  
        asistente = Confirmation.objects.get(act_id = act_id, user_id = user, )
        Aprovar(asistente)
        return redirect('resumen1', act_id=act_id)
    
    return render(request, 'app_visualizacion/resumen1.html', {'datos': datos_acta,
                                                         'desarrollo': datos_desarrollo,
                                                          'asistentes': asistentes,
                                                         'compromisos': compromisos,'act_id':act_id})
def Aprovar(confirmacion):
    confirmacion.approved = True
    confirmacion.save()

def Enviar_Comentario(request, act_id):
    print("aqui")
    if request.method == 'POST':
        comentario = request.POST.get('comentario')
        subject = 'Comentario del Acta'
        message =  comentario
        from_email = 'escuelainteramericanadebibliot@gmail.com'
        # Crea una lista con el correo de destino
        recipient_list = ['escuelainteramericanadebibliot@gmail.com']

        send_mail(subject, message, from_email,  recipient_list)

        
        return redirect('resumen1', act_id=act_id)  # Redirigir a la página de filtrado de actas después de guardar los cambios

    