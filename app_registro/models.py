from django.db import models
# Create your models here.
# Create your models here.
from django.utils import timezone
import datetime

# Create your models here.
class Act(models.Model):
    pub_date = models.DateField()
    process_text = models.CharField(max_length=200)
    type_meet = models.CharField(max_length=20)
    hour = models.TimeField(null=True, default=None)
    next_meet = models.DateField(null=True, default=None)
    next_hour = models.TimeField(null=True, default=None)
    place = models.CharField(max_length=200)
    next_place = models.CharField(max_length=200,null=True, default=None)
    ident = models.IntegerField(null=True, default=None)
    
    def __str__(self):
        return str(self.pk)
    
        
class Job(models.Model):
    name_job = models.CharField(max_length=200)
    description = models.CharField(max_length=200,null=True, default=None)
    
    def __str__(self):
        return str(self.name_job)
  
class User(models.Model):
    name = models.CharField(max_length=200)
    mail = models.CharField(max_length=200,null=True, default=None)
    job_position = models.ForeignKey(Job,on_delete =models.CASCADE,null=True, default=None)
    num_id = models.IntegerField()
    process = models.CharField(max_length=40,null=True, default=None)


    def __str__(self):
        return str(self.num_id)
           
    
class Confirmation(models.Model):
    user_id = models.ForeignKey(User,on_delete =models.CASCADE,verbose_name="Usuario")
    act_id = models.ForeignKey(Act,on_delete =models.CASCADE)
    asset = models.BooleanField(null=True, default=None)

    def __str__(self):
        return str(self.pk)
    
class Commitment(models.Model):
    act_id = models.ForeignKey(Act,on_delete =models.CASCADE,default=None)
    date = models.DateTimeField("Data publish",blank=True,null=True, default=None) 
    observations = models.CharField(max_length=200,null=True, default=None)
    commitment =  models.CharField(max_length=200)
    control =  models.CharField(max_length=200,null=True, default=None)
    user_id = models.ForeignKey(User,on_delete =models.CASCADE,default=None)
    def __str__(self):
        return str(self.pk)
    
class Development(models.Model):
    act_id = models.ForeignKey(Act,on_delete =models.CASCADE)
    num = models.IntegerField(default=None)
    tittle =  models.CharField(max_length=200,null=True, default=None)
    description =  models.CharField(max_length=200,null=True, default=None)
    discussion =  models.CharField(max_length=200,null=True, default=None)
    result =  models.CharField(max_length=200,null=True, default=None)
    user_id = models.ForeignKey(User,on_delete =models.CASCADE,default=None)
    
    def __str__(self):
        return str(self.pk)
    
class Dependece(models.Model):
    cod = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return str(self.pk)
    
class Typemeet(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return str(self.pk)
    
class State(models.Model):
    name = models.CharField(max_length=200,null=True, default=None)
    def __str__(self):
        return str(self.pk)