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
            ), 'process_text': forms.Select(attrs={'class': 'form-control'})
            ,'type_meet': forms.Select(attrs={'class': 'form-control'})
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
        self.fields['send'].required = False
        
        Tiposdereunion = Typemeet.objects.values_list('pk','name')
        self.fields['type_meet'].choices = Tiposdereunion
        Dependecias = Dependece.objects.values_list('pk', 'name')
        self.fields['process_text'].choices = Dependecias
        
   
class RegisterFormUser(forms.ModelForm):
    class Meta:
        """Campos utilizados."""
        model = User
        fields = "__all__"

#para registrar los usuarios en las actas 
class RegisterFormUserConfirmation(forms.ModelForm):
    class Meta:
        """Campos utilizados."""
        model = Confirmation
        fields = "__all__"
        widgets = {
            'asset': forms.CheckboxInput(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['job_position'].required = False

        user = User.objects.values_list('pk','name')
        self.fields['user_id'].choices = user
        job = Job.objects.values_list('pk', 'name_job')
        self.fields['job_position'].choices = job
        proceso = Process.objects.values_list('pk', 'name')
        self.fields['process'].choices = proceso
        
class RegisterFormDevelopment(forms.ModelForm):
    class Meta:
        """Campos utilizados."""
        model = Development
        fields = "__all__"      
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['result'].required = False
        self.fields['discussion'].required = False
        self.fields['num'].required = False
        self.fields['act_id'].required = False
        user = User.objects.values_list('pk','name')
        self.fields['user_id'].choices = user


class RegisterFormCommitment(forms.ModelForm):
    class Meta:
        """Campos utilizados."""
        model = Commitment
        fields = "__all__"
        widgets = {
            'date': NumberInput(attrs={'type':'date'})}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].required = False
        self.fields['observations'].required = False
        self.fields['act_id'].required = False
    

        user = User.objects.values_list('pk','name')
        self.fields['user_id'].choices = user
        controls = State.objects.values_list('pk','name')
        self.fields['control'].choices = controls

class RegisterFormAssistant(forms.ModelForm):
    class Meta:
        """Campos utilizados."""
        model = User
        fields = "__all__"
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['name'].required = False
            self.fields['mail'].required = False
            self.fields['num_id'].required = False
        
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
            'type_meet': forms.Select(attrs={'class': 'form-control'}),
            'process_text': forms.Select(attrs={'class': 'form-control'}),

        }
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['pub_date'].required = False
            self.fields['process_text'].required = False
            self.fields['hour'].required = False
            self.fields['next_meet'].required = False
            self.fields['next_hour'].required = False
            self.fields['place'].required = False
            self.fields['ident'].required = False
            self.fields['send'].required = False
            self.fields['next_place'].required = False
            Tiposdereunion = Typemeet.objects.values_list('pk','name')
            self.fields['type_meet'].widget.choices = Tiposdereunion
            Dependecias = Dependece.objects.values_list('cod', 'name')
            self.fields['process_text'].widget.choices = Dependecias

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['name'].required = False
            self.fields['mail'].required = False
            self.fields['num_id'].required = False

class ProcessForm(forms.ModelForm):
    class Meta:
        model = Dependece
        fields = "__all__"

class TypeMeetForm(forms.ModelForm):
    class Meta:
        model = Typemeet
        fields = "__all__"
   