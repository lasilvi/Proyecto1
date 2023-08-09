
# Create your views here.
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import *
from django.urls import reverse
from .models import *
from .models import Development
from django.views import View
import json
from django.db.models import Max,Q
from django.http import JsonResponse
from django.contrib import messages 
from django.core.mail import send_mail

# Create your views here.

class MenuView(View):
    def get(self, request):
        return render(request, 'app_registro/menu.html')
    def post(self, request):
        # Lógica para procesar las solicitudes POST
        # ...
        return render(request, 'app_registro/formulario.html')
    
def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
       
        if form.is_valid():
           print("aqui")
           act = form.save(commit=False)
            # Obtener el tipo de dependencia seleccionado en el formulario
           tipo_dependencia = form.cleaned_data['process_text']
           tipo_reunion = form.cleaned_data['type_meet']
             
           resultados = Act.objects.filter(Q(process_text=tipo_dependencia) & Q(type_meet=tipo_reunion))
           ultimo_ident_dict = resultados.aggregate(Max('ident'))
           ultimo_ident = ultimo_ident_dict['ident__max']

            # Incrementar el valor de 'ident' para la nueva Acta
           if ultimo_ident is not None:
                act.ident = ultimo_ident + 1
           else:
                act.ident = 1
                
           act.save()
           id = str(act.pk)
           indentificacion = act.ident
           proceso = str(act.process_text)
           resultados = Dependece.objects.filter(cod=proceso)
           if resultados.exists():
                primer_resultado = resultados.first()  # Obtener el primer objeto del queryset
                act_proceso_name = primer_resultado.name
           else:
                # Manejar el caso cuando no hay resultados encontrados
                act_proceso_name = None
           # Construye la URL de redirección con la variable como parámetro
           url_redireccion = reverse('RegistroUserconfirmation' , kwargs={'act_id': id, 'act_proceso': proceso, 'act_ident': indentificacion})
           return redirect(url_redireccion) 
        else:
            errors = form.errors
            print(errors)
    else:
    
        form = RegisterForm()
        #formuser = RegisterFormUser()
    return render(request, 'app_registro/formulario.html', {'form': form})

#/////////////////////////////////////////////////////////////////////////////////
def RegisterUserConfirmation(request,act_id,act_proceso,act_ident):
    if request.method == 'POST':
        formuser = RegisterFormUserConfirmation(request.POST)
        

        if formuser.is_valid():
            
            user_id = formuser.cleaned_data['user_id']  # Obtener el ID del usuario del formulario
            existing_confirmation = Confirmation.objects.filter(act_id=act_id, user_id=user_id).first()
            if existing_confirmation:
                # Si ya existe, redirigir a la página de confirmación con un mensaje de error
                messages.error(request, 'El asistente ya ha sido registrado para esta acta.')
                url_redireccion = reverse('RegistroUserconfirmation' , kwargs={'act_id': act_id, 'act_proceso': act_proceso, 'act_ident': act_ident})
                return redirect(url_redireccion)
            
            confirmacion = formuser.save(commit=False)
            confirmacion.save()

            # Construye la URL de redirección con la variable como parámetro
            url_redireccion = reverse('RegistroUserconfirmation' , kwargs={'act_id': act_id, 'act_proceso': act_proceso, 'act_ident': act_ident})
            return redirect(url_redireccion) 
            
    else:
        formuser = RegisterFormUserConfirmation()
    confimaciones = Confirmation.objects.filter(act_id=act_id)
    proceso = Dependece.objects.get(cod=act_proceso)
    context = {
    'form': formuser,
    'act_id': act_id,
    'act_proceso': act_proceso,
    'act_ident': act_ident,
    'confimaciones':confimaciones,
    'proceso': proceso,

    }
    
    return render(request, 'app_registro/formulario2.html', context)

def editar_RegisterUserConfirmation(request,user_id,act_id,act_proceso,act_ident):
    confimaciones = Confirmation.objects.get(id=user_id)
    
    if request.method == 'POST':
        form = RegisterFormUserConfirmation(request.POST, instance=confimaciones)
        #if form.is_valid():
        # Actualizar
        #  otros campos según sea necesario
        form.save()
        url= reverse('RegistroUserconfirmation', kwargs={'act_id': act_id, 'act_proceso': act_proceso, 'act_ident': act_ident}) 
        return redirect(url) # Redirigir a la página de filtrado de actas después de guardar los cambios
    else:
        form = RegisterFormUserConfirmation(instance=confimaciones)
    context = {
        'form': form,
    }

    return render(request, ('app_registro/editar_formulario2confirmacion.html'), context)

def eliminar_RegisterUserConfirmation(request,user_id,act_id,act_proceso,act_ident):
    print(user_id)
    
    if request.method == 'GET':
        confirmation = Confirmation.objects.get(id=user_id)
        return render(request, 'app_registro/eliminar_RegistroUsuariosConfirmacion.html', {'confirmation': confirmation, 'act_id': act_id,
    'act_proceso': act_proceso,
    'act_ident': act_ident})

    elif request.method == 'POST':
        confirmation = Confirmation.objects.get(id=user_id)
        confirmation.delete()
        # Construye la URL de redirección con la variable como parámetro
        url_redireccion = reverse('RegistroUserconfirmation' , kwargs={'act_id': act_id, 'act_proceso': act_proceso, 'act_ident': act_ident})
        return redirect(url_redireccion) 
        
#////////////////////////////////////////////////////////////////////////////////
def RegisterDevelopment(request,act_id,act_proceso,act_ident):
    if request.method == 'POST':
        formdevelopment = RegisterFormDevelopment(request.POST)
        if formdevelopment.is_valid():
            desarrollo = formdevelopment.save(commit=False)
            
            # Obtener el último valor de "num" para la combinación de "act_id" y "desarrollo"
            last_development = Development.objects.filter(act_id=act_id).order_by('-num').first()
            if last_development:
                new_num = last_development.num + 1
            else:
                new_num = 1
                
            desarrollo.num = new_num

            desarrollo.save()
                
            url_redireccion = reverse('RegistroDevelop' , args=[act_id, act_proceso, act_ident])
            return redirect(url_redireccion)  
        else:
            # Mensajes de depuración para ver los errores del formulario en la consola
            print("Errores del formulario:")
            print(formdevelopment.errors)
    else:
        formdevelopment = RegisterFormDevelopment()
    desarrollo = Development.objects.filter(act_id=act_id)
    proceso = Dependece.objects.get(cod=act_proceso)
    context = {
            'form': formdevelopment,'act_id': act_id,'act_proceso': act_proceso,
            'act_ident': act_ident,'desarrollo':desarrollo,'proceso': proceso}    
    return render(request, 'app_registro/formulario3.html',  context )

def eliminar_RegisterDevelopment(request,desarrollo_id,act_id,act_proceso,act_ident):
    print(desarrollo_id)
    
    if request.method == 'GET':
        desarrollo = Development.objects.get(id=desarrollo_id)
        return render(request, 'app_registro/eliminar_Desarrollo.html', {'desarrollo': desarrollo, 'act_id': act_id,'act_proceso': act_proceso,'act_ident': act_ident})

    elif request.method == 'POST':
        desarrollo = Development.objects.get(id=desarrollo_id)
        desarrollo.delete()
        # Construye la URL de redirección con la variable como parámetro
        url_redireccion = reverse('RegistroDevelop' , args=[act_id, act_proceso, act_ident]) 
        return redirect(url_redireccion) 

def editar_RegisterDevelopment(request,desarrollo_id,act_id,act_proceso,act_ident):
    desarrollo = Development.objects.get(id=desarrollo_id)
    
    if request.method == 'POST':
        form = RegisterFormDevelopment(request.POST, instance=desarrollo)
        #if form.is_valid():
        # Actualizar
        #  otros campos según sea necesario
        form.save()
        url= reverse('RegistroDevelop', kwargs={'act_id': act_id, 'act_proceso': act_proceso, 'act_ident': act_ident}) 
        return redirect(url) # Redirigir a la página de filtrado de actas después de guardar los cambios
    else:
        form = RegisterFormDevelopment(instance=desarrollo)
    context = {
        'form': form,
    }

    return render(request, ('app_registro/editar_formulario3desarrollo.html'), context)
#///////////////////////////////////////////////////////////////////////////////////////////////
def RegisterCommintment(request,act_id,act_proceso,act_ident):
    if request.method == 'POST':
        formcompromiso = RegisterFormCommitment(request.POST)
        if formcompromiso.is_valid():
            compromiso = formcompromiso.save(commit=False)
            act_instance = Act.objects.get(id=act_id)
            compromiso.act_id = act_instance
            compromiso.save()
                
            url_redireccion = reverse('RegistroCommintment', args=[act_id, act_proceso, act_ident])
            return redirect(url_redireccion) 
        else:
            # Mensajes de depuración para ver los errores del formulario en la consola
            print("Errores del formulario:")
            print(formcompromiso.errors) 
    else:
        formcompromiso = RegisterFormCommitment()
    compromisos = Commitment.objects.filter(act_id=act_id)
    proceso = Dependece.objects.get(cod=act_proceso)
    context = {
            'form': formcompromiso,'act_id': act_id,'act_proceso': act_proceso,
            'act_ident': act_ident,'compromiso':compromisos,'proceso': proceso}    
    return render(request, 'app_registro/formulario4.html',  context )

def eliminar_RegisterCommintment(request,compromiso_id,act_id,act_proceso,act_ident):

    if request.method == 'GET':
        compromiso = Commitment.objects.get(id=compromiso_id)
        return render(request, 'app_registro/eliminar_Compromiso.html', {'compromiso': compromiso, 'act_id': act_id,'act_proceso': act_proceso,'act_ident': act_ident})

    elif request.method == 'POST':
        desarrollo = Commitment.objects.get(id=compromiso_id)
        desarrollo.delete()
        # Construye la URL de redirección con la variable como parámetro
        url_redireccion = reverse('RegistroCommintment' , args=[act_id, act_proceso, act_ident]) 
        return redirect(url_redireccion) 
    
def editar_RegisterCommintment(request,compromiso_id,act_id,act_proceso,act_ident):
    compromiso = Commitment.objects.get(id=compromiso_id)
    
    if request.method == 'POST':
        form = RegisterFormCommitment(request.POST, instance=compromiso)
        #if form.is_valid():
        # Actualizar
        #  otros campos según sea necesario
        form.save()
        url= reverse('RegistroCommintment', kwargs={'act_id': act_id, 'act_proceso': act_proceso, 'act_ident': act_ident}) 
        return redirect(url) # Redirigir a la página de filtrado de actas después de guardar los cambios
    else:
        form = RegisterFormCommitment(instance=compromiso)
    context = {
        'form': form,
    }

    return render(request, ('app_registro/editar_formulario4compromiso.html'), context)
#////////////////////////////////////////////////////////////////////////////////
def RegisterAssistant(request):
    if request.method == 'POST':
        form = RegisterFormAssistant(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('RegisterAssistant') 
    else:
        form = RegisterFormAssistant()      
    users = User.objects.all()
    context = {
            'form': form ,
            'users' : users   }     
    return render(request, 'app_registro/usuarios.html', context)

def eliminar_usuario(request,user_id):

    if request.method == 'GET':
        user = User.objects.get(pk=user_id)
        return render(request, 'app_registro/eliminar_usuario.html', {'user': user})

    elif request.method == 'POST':
        user = User.objects.get(pk=user_id)
        user.delete()
        return redirect('RegisterAssistant')

def editar_usuario(request, user_id):
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        #if form.is_valid():
        # Actualizar otros campos según sea necesario
        form.save()
        return redirect('RegisterAssistant')  # Redirigir a la página de filtrado de actas después de guardar los cambios
    else:
        form = UserForm(instance=user)
    context = {
        'form': form,
    }

    return render(request, ('app_registro/editar_usuario.html'), context)

#///////////////////////////////////////////////////////////////////////////////
def RegisterProcess(request):
    if request.method == 'POST':
        form = ProcessForm(request.POST)
        if form.is_valid():
            process = form.save()
            return redirect('RegisterProcess')
    else:     
        form = ProcessForm()
    processs = Dependece.objects.all()
    context = {
        'form': form ,
        'processs' : processs}     
    return render(request, 'app_registro/procesos.html', context)

def editar_Proceso(request, process_id):
    process = Dependece.objects.get(id=process_id)
    
    if request.method == 'POST':
        form = ProcessForm(request.POST, instance=process)
        #if form.is_valid():
        # Actualizar
        #  otros campos según sea necesario
        form.save()
        return redirect('RegisterProcess')  # Redirigir a la página de filtrado de actas después de guardar los cambios
    else:
        form = ProcessForm(instance=process)
    context = {
        'form': form,
    }

    return render(request, ('app_registro/editar_procesos.html'), context)

def eliminar_proceso(request,dependece_id):

    if request.method == 'GET':
        dependece = Dependece.objects.get(pk=dependece_id)
        return render(request, 'app_registro/eliminar_proceso.html', {'depedece': dependece})

    elif request.method == 'POST':
        dependece = Dependece.objects.get(pk=dependece_id)
        dependece.delete()
        return redirect('RegisterProcess')

#///////////////////////////////////////////////////////////////////////////////
def RegisterTypemeet(request):
    if request.method == 'POST':
        form = TypeMeetForm(request.POST)
        if form.is_valid():
            typemeet = form.save()
          
    form = TypeMeetForm()
    typemeets = Typemeet.objects.all()
    context = {
        'form': form ,
        'typemeets' : typemeets}     
    return render(request, 'app_registro/tipodereunion.html', context)

def editar_Tipodereunion(request, tmeet_id):
    typemeet = Typemeet.objects.get(id=tmeet_id)
    
    if request.method == 'POST':
        form = TypeMeetForm(request.POST, instance=typemeet)
        #if form.is_valid():
        # Actualizar
        #  otros campos según sea necesario
        form.save()
        return redirect('RegisterTypemeet')  # Redirigir a la página de filtrado de actas después de guardar los cambios
    else:
        form = TypeMeetForm(instance=typemeet)
    context = {
        'form': form,
    }

    return render(request, ('app_registro/editar_tipodereunion.html'), context)

def eliminar_tipo_reunion(request,type_id):

    if request.method == 'GET':
        typemeet = Typemeet.objects.get(pk=type_id)
        return render(request, 'app_registro/eliminar_tipo_reunion.html', {'typemeet': typemeet})

    elif request.method == 'POST':
        typemeet = Typemeet.objects.get(pk=type_id)
        typemeet.delete()
        return redirect('RegisterTypemeet')

#///////////////////////////////////////////////////////////////////////////////
def edit_act(request, act_id):
    acta = Act.objects.get(id=act_id)
    confirmacion = Confirmation.objects.filter(act_id=act_id)
    desarrollo = Development.objects.filter(act_id=act_id)
    compromisos = Commitment.objects.filter(act_id=act_id)

    nombreproceso = acta.process_text
    if request.method == 'POST':

        form = ActForm(request.POST, instance=acta)

        if form.is_valid():
            tipo_dependencia = form.cleaned_data['process_text']
            tipo_reunion = form.cleaned_data['type_meet']
                
            resultados = Act.objects.filter(Q(process_text=tipo_dependencia) & Q(type_meet=tipo_reunion))
            ultimo_ident_dict = resultados.aggregate(Max('ident'))
            ultimo_ident = ultimo_ident_dict['ident__max']

            # Incrementar el valor de 'ident' para la nueva Acta
            if ultimo_ident is not None:
                acta.ident = ultimo_ident + 1
                print(acta.ident)
            else:
                acta.ident = 1
                print(acta.ident)
            #if form.is_valid():
            # Actualizar otros campos según sea necesario
            form.save()
            acta.save()
            print("si")
            url_redireccion = reverse('edit_act' , args=[act_id])
            return redirect(url_redireccion)  # Redirigir a la página de filtrado de actas después de guardar los cambios
    else:
        form = ActForm(instance=acta)
    context = {
        'form': form,
        'acta': acta,
        'confirmacion': confirmacion,
        'desarrollos': desarrollo,
        'compromisos': compromisos,
        'proceso':nombreproceso
    }
    print("no")
    return render(request, 'app_registro/edit_act.html', context)

def Summary(request,act_id):
    # Realiza la consulta y el filtrado de los datos
    datos_acta = Act.objects.filter(pk=act_id)
    datos_desarrollo = Development.objects.filter(act_id=act_id)
    for dato in datos_acta:
      ProcesoDependecia = dato.process_text
      Tipodereunion = dato.type_meet
      
    nombreproceso = Dependece.objects.filter(cod=ProcesoDependecia)
    nombretiporeunion = Typemeet.objects.filter(pk=Tipodereunion)
    asistentes = Confirmation.objects.filter(act_id = act_id)
    compromisos = Commitment.objects.filter(act_id=act_id)
    
    if request.method == 'POST':
        acta = get_object_or_404(Act, pk=act_id)
        acta.send = True
        acta.save()
        contenido_correo = "hola"
        correos_destino =  [asistente.user_id.mail for asistente in asistentes if asistente.user_id.mail]
        # Enviar el correo a cada dirección de correo electrónico
        for correo_destino in correos_destino:
            enviar_correo(correo_destino, contenido_correo)

        return redirect('resumen', act_id=act_id)

    return render(request, 'app_registro/resumen.html', {'datos': datos_acta,
                                                         'desarrollo': datos_desarrollo,'nombreproceso' : nombreproceso,
                                                         'nombretiporeunion':nombretiporeunion, 'asistentes': asistentes,
                                                         'compromisos': compromisos,'act_id':act_id})

def filter_acts(request):
    ident = request.POST.get('ident')
    date = request.POST.get('date')
    type_meet = request.POST.get('type_meet')

    acts = Act.objects.all()

    if ident:
        acts = acts.filter(ident=ident)
    if date:
        acts = acts.filter(pub_date=date)
    if type_meet:
        acts = acts.filter(type_meet=type_meet)

    typemeets = Typemeet.objects.all()
    Dependeces = Dependece.objects.all()

    context = {
        'acts': acts,
        'typemeets': typemeets,
        'Dependeces': Dependeces,
    }

    return render(request, 'app_registro/filter_acts.html', context)


def enviar_correo(correo_destino,contenido_correo):
    subject = 'Asunto del correo'
    message = contenido_correo
    from_email = 'tu_correo@example.com'
     # Crea una lista con el correo de destino
    recipient_list = [correo_destino]

    send_mail(subject, message, from_email,  recipient_list)

    # Opcionalmente, puedes redireccionar a una página de éxito o renderear un template de éxito
    #return render(request, 'correo_enviado.html')

    

    
