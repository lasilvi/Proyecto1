from django.db import models
# Create your models here.
# Create your models here.
from django.utils import timezone
import datetime

class Dependece(models.Model):
    cod = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return str(self.cod)
    
class Typemeet(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return str(self.pk)
# Create your models here.
class Act(models.Model):
    pub_date = models.DateField()
    process_text = models.ForeignKey(Dependece,on_delete =models.CASCADE,default=None)
    type_meet = models.ForeignKey(Typemeet,on_delete =models.CASCADE,default=None)
    hour = models.TimeField(null=True)
    next_meet = models.DateField(null=True)
    next_hour = models.TimeField(null=True )
    place = models.CharField(max_length=200, editable=True)
    next_place = models.CharField(max_length=200,null=True)
    ident = models.IntegerField(null=True, default=None)
    send = models.BooleanField(null=True, default=None)
  
    def __str__(self):
        return str(self.pk)
class Comentario(models.Model):
    act_id = models.ForeignKey(Act,on_delete =models.CASCADE)
    comentario = models.CharField(max_length=200000,null=True, default=None)
        
class Job(models.Model):
    name_job = models.CharField(max_length=200)
    description = models.CharField(max_length=200,null=True, default=None)
    
    def __str__(self):
        return str(self.name_job)
  
class User(models.Model):
    name = models.CharField(max_length=200, default=None)
    mail = models.CharField(max_length=200,null=True,default=None)
    num_id = models.IntegerField(default=None)
    
 

    def __str__(self):
        return str(self.num_id)
           
class Process(models.Model):
    name = models.CharField(max_length=200,null=True, default=None)
    def __str__(self):
        return str(self.name)
    
class Confirmation(models.Model):
    user_id = models.ForeignKey(User,on_delete =models.CASCADE,verbose_name="Usuario")
    act_id = models.ForeignKey(Act,on_delete =models.CASCADE)
    asset = models.BooleanField(null=True, default=None)
    job_position = models.ForeignKey(Job, on_delete=models.SET_NULL, blank=True, null=True)
    process = models.ForeignKey(Process,on_delete =models.CASCADE,null=True, default=None)
    approved = models.BooleanField(null=True, default=False)

    def __str__(self):
        return str(self.pk)
    
class State(models.Model):
    name = models.CharField(max_length=500,null=True, default=None)
    def __str__(self):
        return str(self.pk)
    
class Commitment(models.Model):
    act_id = models.ForeignKey(Act,on_delete =models.CASCADE,default=None)
    date = models.DateTimeField("Data publish",blank=True,null=True, default=None) 
    observations = models.CharField(max_length=20000)
    commitment =  models.CharField(max_length=200000)
    user_id = models.ForeignKey(User,on_delete =models.CASCADE)
    control =  models.ForeignKey(State,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.pk)
    
class Development(models.Model):
    act_id = models.ForeignKey(Act,on_delete =models.CASCADE)
    num = models.IntegerField(default=None)
    tittle =  models.CharField(max_length=2000,null=True, default=None)
    description =  models.CharField(max_length=20000,null=True, default=None)
    discussion =  models.CharField(max_length=20000,null=True)
    result =  models.CharField(max_length=20000,null=True)
    user_id = models.ForeignKey(User,on_delete =models.CASCADE,default=None)
    
    def __str__(self):
        return str(self.pk)
    

    
