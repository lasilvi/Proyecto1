
# Create your views here.
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import *
from django.urls import reverse
from .models import *
from .models import Development
from django.views import View
import json
from django.db.models import Max,Q

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
           indentificacion = str(act.ident)
           proceso = str(act.process_text)
           resultados = Dependece.objects.filter(cod=proceso)
           if resultados.exists():
                primer_resultado = resultados.first()  # Obtener el primer objeto del queryset
                act_proceso_name = primer_resultado.name
           else:
                # Manejar el caso cuando no hay resultados encontrados
                act_proceso_name = None
           # Construye la URL de redirección con la variable como parámetro
           url_redireccion = reverse('RegistroUserconfirmation') + '?ActaN°=' + id + '&Proceso/Dependecia=' + act_proceso_name + '&Identificacion=' + indentificacion
           return redirect(url_redireccion) 
    else:
        form = RegisterForm()
        #formuser = RegisterFormUser()
    return render(request, 'app_registro/formulario.html', {'form': form})

def RegisterUserConfirmation(request):
    act_id = int(request.GET.get("ActaN°"))
    act_proceso = request.GET.get("Proceso/Dependecia")
    act_ident = request.GET.get("Identificacion")
    if request.method == 'POST':
        formuser = RegisterFormUserConfirmation(request.POST)
        # Obtener el diccionario valoresCampos del formulario
        valoresCampos = request.POST.get('valoresCampos')
        if valoresCampos:
            valoresCampos = json.loads(valoresCampos)
            # Procesar los usuarios del diccionario valoresCampos
            
            for  user_id, valor in valoresCampos.items():
                print(valor[0])
                print(valor[1])
                print(valor[2])
                print(valor[3])
                print(user_id)
                try:
                    act_instance = Act.objects.get(id=act_id)
                    user_instance = User.objects.get(num_id=int(valor[0]))
                    job_instance = Job.objects.get(pk=int(valor[2]))
                    Process_instance = Process.objects.get(pk=int(valor[3]))
                
                except Act.DoesNotExist:
                    return HttpResponse('No se encontró el Act correspondiente')
                except User.DoesNotExist:
                    return HttpResponse(f"No se encontró el usuario con ID {user_id}")

                confirmation = Confirmation()
                confirmation.act_id = act_instance
                confirmation.user_id = user_instance
                confirmation.asset = valor[1]
                confirmation.job_position = job_instance
                confirmation.process = Process_instance
                confirmation.save()
            url_redireccion = reverse('RegistroDevelop') + '?ActaN°=' + str(act_id) + '&Proceso/Dependecia=' + act_proceso + '&Identificacion=' + act_ident
            return redirect(url_redireccion) 
    else:
        formuser = RegisterFormUserConfirmation()
    context = {
    'form': formuser,
    'act_id': act_id,
    'act_proceso': act_proceso,
    'act_ident': act_ident,
    }
    
    return render(request, 'app_registro/formulario2.html', context)

def RegisterDevelopment(request):
    act_id = int(request.GET.get("ActaN°"))
    act_proceso = request.GET.get("Proceso/Dependecia")
    act_ident = request.GET.get("Identificacion")
    if request.method == 'POST':
        formdevelopment = RegisterFormDevelopment(request.POST)

        valoresCampos = request.POST.get('valoresCampos')
        if valoresCampos:
            valoresCampos = json.loads(valoresCampos)
            # Procesar los usuarios del diccionario valoresCampos
            for  num, valor in valoresCampos.items():
                try:
                    act_instance = Act.objects.get(id=act_id)
                    user_instance = User.objects.get(num_id=int(valor[1]))
                    print(valor[0])
                    print(valor[1])
                    print(valor[2])
                    print(valor[3])
                    print(valor[4])
                    print(valor[5])
                
                except Act.DoesNotExist:
                    return HttpResponse('No se encontró el Act correspondiente')
                except User.DoesNotExist:
                    return HttpResponse(f"No se encontró el usuario con ID {num}")

                Development_instance = Development()
                Development_instance = Development()
                Development_instance.act_id = act_instance
                Development_instance.num = valor[0]
                Development_instance.tittle = valor[2]
                Development_instance.description = valor[3]
                Development_instance.discussion = valor[4]
                Development_instance.result = valor[5]
                Development_instance.user_id = user_instance
                Development_instance.save()

            url_redireccion = reverse('RegistroCommintment') + '?ActaN°=' + str(act_id) + '&Proceso/Dependecia=' + act_proceso + '&Identificacion=' + act_ident
            return redirect(url_redireccion) 
    else:
        formdevelopment = RegisterFormDevelopment()
    context = {
            'form': formdevelopment,
            'act_id': act_id,
            'act_proceso': act_proceso,
            'act_ident': act_ident,
        }    
    return render(request, 'app_registro/formulario3.html',  context )

def RegisterCommintment(request):
    act_id = int(request.GET.get("ActaN°"))
    act_proceso = request.GET.get("Proceso/Dependecia")
    act_ident = request.GET.get("Identificacion")
    if request.method == 'POST':
        form = RegisterFormCommitment(request.POST)
        valoresCampos = request.POST.get('valoresCampos')
        if valoresCampos:
            valoresCampos = json.loads(valoresCampos)
            # Procesar los usuarios del diccionario valoresCampos
            for  num, valor in valoresCampos.items():
                try:
                    act_instance = Act.objects.get(id=act_id)
                    user_instance = User.objects.get(num_id=int(valor[1]))   
                    state_instance = State.objects.get(pk= int(valor[4]))
                except Act.DoesNotExist:
                    return HttpResponse('No se encontró el Act correspondiente')
                except User.DoesNotExist:
                    return HttpResponse(f"No se encontró el usuario con ID {num}")

                comimtment_instance = Commitment()
                comimtment_instance.act_id = act_instance
                comimtment_instance.user_id = user_instance
                comimtment_instance.date = valor[3]
                comimtment_instance.observations = valor[2]
                comimtment_instance.commitment = valor[5]
                comimtment_instance.control = state_instance
                comimtment_instance.save()

            url_redireccion = reverse('resumen') + '?ActaN°=' + str(act_id)
            return redirect(url_redireccion)
    else:
        form = RegisterFormCommitment()
        context = {
        'form': form,
        'act_id': act_id,
        'act_proceso': act_proceso,
        'act_ident': act_ident,
            }     
        return render(request, 'app_registro/formulario4.html', context)

def RegisterAssistant(request):
    if request.method == 'POST':
        form = RegisterFormAssistant(request.POST)
        if form.is_valid():
            user = form.save()
            url_redireccion = reverse('menu') 
            return redirect(url_redireccion)
    else:
        form = RegisterFormAssistant()
        context = {
        'form': form     }     
        return render(request, 'app_registro/usuarios.html', context)


def edit_act(request, act_id):
    acta = Act.objects.get(id=act_id)

    if request.method == 'POST':
        # Manejar el envío del formulario y actualizar los campos del acta en consecuencia
        acta.campo1 = request.POST.get('campo1')
        acta.campo2 = request.POST.get('campo2')
        # Actualizar otros campos según sea necesario
        acta.save()
        return redirect('filter_acts')  # Redirigir a la página de filtrado de actas después de guardar los cambios

    context = {
        'acta': acta
    }

    return render(request, 'app_registro/edit_act.html', context)

def Summary(request):
    # Obtén el valor del campo por el cual deseas filtrar (puedes pasarlo a través de la URL o de un formulario)
    valor_act = int(request.GET.get("ActaN°"))
    # Realiza la consulta y el filtrado de los datos
    datos_acta = Act.objects.filter(pk=valor_act)
    datos_desarrollo = Development.objects.filter(act_id=valor_act)
    for dato in datos_acta:
      ProcesoDependecia = dato.process_text
      Tipodereunion = dato.type_meet
      
    nombreproceso = Dependece.objects.filter(cod=ProcesoDependecia)
    nombretiporeunion = Typemeet.objects.filter(pk=Tipodereunion)
    asistentes = Confirmation.objects.filter(act_id = valor_act)
    
    return render(request, 'app_registro/resumen.html', {'datos': datos_acta,'desarrollo': datos_desarrollo,'nombreproceso' : nombreproceso,'nombretiporeunion':nombretiporeunion, 'asistentes': asistentes})

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

    context = {
        'acts': acts,
        'typemeets': typemeets
    }

    return render(request, 'app_registro/filter_acts.html', context)
