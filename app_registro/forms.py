from django import forms
from .models import *
from django.forms import formset_factory
from django.forms.widgets import NumberInput

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
        Dependecias = Dependece.objects.values_list('cod', 'name')
        self.fields['process_text'].choices = Dependecias
        Tiposdereunion = Typemeet.objects.values_list('pk','name')
        self.fields['type_meet'].choices = Tiposdereunion
   
        
class RegisterFormUser(forms.ModelForm):
    class Meta:
        """Campos utilizados."""
        model = User
        fields = "__all__"

#para registrar los usuarios en las actas 
class RegisterFormUserConfirmation(forms.Form):
    users = User.objects.values_list('num_id','name')
    user = forms.ChoiceField(choices=users)

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
    class Meta:
        """Campos utilizados."""
        model = Commitment
        fields = "__all__"
        widgets = {
            'date': NumberInput(attrs={'type':'date'})}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].required = False
        
        