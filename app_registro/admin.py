from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

class ActAdmin(admin.ModelAdmin):
    list_display = [field.name for field in  Act._meta.fields]
admin.site.register(Act, ActAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]
admin.site.register(User, UserAdmin)
# Register your models here.

class JobAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Job._meta.fields]
admin.site.register(Job, JobAdmin)
# Register your models here.

class ConfirmationAdmin(admin.ModelAdmin):
   list_display = [field.name for field in Confirmation._meta.fields]
admin.site.register(Confirmation, ConfirmationAdmin)
# Register your models here.

class CommitmentAdmin(admin.ModelAdmin):
   list_display = [field.name for field in Commitment._meta.fields]
admin.site.register( Commitment, CommitmentAdmin)

class DevelopmentAdmin(admin.ModelAdmin):
   list_display = [field.name for field in Development._meta.fields]
admin.site.register(Development, DevelopmentAdmin)

class TypemeetAdmin(admin.ModelAdmin):
   list_display = [field.name for field in Typemeet._meta.fields]
admin.site.register(Typemeet, TypemeetAdmin)

class DependeceAdmin(admin.ModelAdmin):
   list_display = [field.name for field in Dependece._meta.fields]
admin.site.register(Dependece, DependeceAdmin)

class StateAdmin(admin.ModelAdmin):
   list_display = [field.name for field in State._meta.fields]
admin.site.register(State, StateAdmin)

class ProcessAdmin(admin.ModelAdmin):
   list_display = [field.name for field in Process._meta.fields]
admin.site.register(Process, ProcessAdmin)