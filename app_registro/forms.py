from django import forms
from .models import *
from django.forms import formset_factory
from django.forms.widgets import NumberInput
from django.forms.widgets import TextInput, DateInput, TimeInput

class RegisterForm(forms.ModelForm):
    class Meta:
        """Campos utilizados."""
        model = Act
        fields = "__all__"
        widgets = {
            'next_meet': NumberInput(attrs={'type':'date'}),
            'pub_date': NumberInput(attrs={'type':'date'}),
            'hour': forms.TimeInput(
                format=("%H:%M"),
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a date",
                    "type": "time",
                },
            ),
             'next_hour': forms.TimeInput(
                format=("%H:%M"),
                attrs={
                    "class": "form-control",
                    "placeholder": "Select a date",
                    "type": "time",
                },
            )
            #'next_meet': NumberInput(attrs={'type':'date'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hour'].required = False
        self.fields['next_meet'].required = False
        self.fields['next_hour'].required = False
        self.fields['place'].required = False
        self.fields['next_place'].required = False
        self.fields['ident'].required = False
        Tiposdereunion = Typemeet.objects.values_list('pk','name')
        print(Tiposdereunion)
        self.fields['type_meet'].choices = Tiposdereunion
        Dependecias = Dependece.objects.values_list('cod', 'name')
        self.fields['process_text'].choices = Dependecias
        
   
class RegisterFormUser(forms.ModelForm):
    class Meta:
        """Campos utilizados."""
        model = User
        fields = "__all__"

#para registrar los usuarios en las actas 
class RegisterFormUserConfirmation(forms.Form):
    users = User.objects.values_list('num_id','name')
    user = forms.ChoiceField(choices=users)
    jobs = Job.objects.values_list('pk','name_job')
    job = forms.ChoiceField(choices=jobs)
    procesos = Process.objects.values_list('pk','name')
    proceso = forms.ChoiceField(choices=procesos)

    class Meta:
        """Campos utilizados."""
        model = Commitment
        fields = "__all__"
        widgets = {
            'date': NumberInput(attrs={'type': 'date'}),
        }

ConfirmationFormSet = formset_factory(RegisterFormUserConfirmation)    
    
class RegisterFormDevelopment(forms.ModelForm):
    responsibles = User.objects.values_list('num_id','name')
    responsible = forms.ChoiceField(choices=responsibles)
    class Meta:
        """Campos utilizados."""
        model = Development
        fields = "__all__"      
DevelopmentFormSet = formset_factory(RegisterFormDevelopment)

class RegisterFormCommitment(forms.ModelForm):
    responsibles = User.objects.values_list('num_id','name')
    responsible = forms.ChoiceField(choices=responsibles)
    controls = State.objects.values_list('pk','name')
    estado = forms.ChoiceField(choices=controls)
    print(estado)
    class Meta:
        """Campos utilizados."""
        model = Commitment
        fields = "__all__"
        widgets = {
            'date': NumberInput(attrs={'type':'date'})}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].required = False

class RegisterFormAssistant(forms.ModelForm):
    cargos = User.objects.values_list('num_id','name')
    cargo = forms.ChoiceField(choices=cargos)
    class Meta:
        """Campos utilizados."""
        model = User
        fields = "__all__"
        
class ActForm(forms.ModelForm):
    class Meta:
        model = Act
        fields = "__all__"
        widgets = {
            'pub_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hour': TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'place': TextInput(attrs={'class': 'form-control'}),
            'next_meet': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'next_hour': TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'next_place': TextInput(attrs={'class': 'form-control'}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['pub_date'].required = False
            self.fields['process_text'].required = False
            self.fields['type_meet'].required = False
            self.fields['ident'].required = False
            self.fields['hour'].required = False
            self.fields['next_meet'].required = False
            self.fields['next_hour'].required = False
            self.fields['place'].required = False
            self.fields['next_place'].required = False