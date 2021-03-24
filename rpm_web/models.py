from django.db import models

# Create your models here.
from django.utils.timezone import datetime #important if using timezones
from datetime import date
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

#Para utilizar usuarios de Django:
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator, MinValueValidator 

#------------------------------------------------------------------------
#-----------new relacionales---------------------------------------------
#------------------------------------------------------------------------

class MType_input2(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length = 50,default='',blank=True)
    comment = models.CharField(max_length = 200,default='',blank=True)
    #graphic
    fig1_name= models.CharField(max_length = 100,default='pptx.ShapeType.ellipse',blank=True)
    fig1_s= models.FloatField(default=0.28)
   
    class Meta: # This class will let you force the name of the table to what you like.
        db_table = "Type_input2"
       
    def get_name(self):
        return self.name

    def __str__(self):
        return '%s, %s' % (self.id, self.name)

class MPlan2(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length = 50,default='',blank=True)
    comment = models.CharField(max_length = 200,default='',blank=True)
    #graphic
    fig1_color_1 = models.CharField(max_length = 10,default='#dc143c',blank=True) #fill color
    fig1_color_2 = models.CharField(max_length = 10,default='#000000',blank=True) #border color
    fig1_color_3 = models.CharField(max_length = 10,default='#dc143c',blank=True)
    fig1_border_w = models.FloatField(default=1)
   
    class Meta: # This class will let you force the name of the table to what you like.
        db_table = "Plan2"
       
    def get_name(self):
        return self.name

    def __str__(self):
        return '%s, %s' % (self.id, self.name)

class MConfig_prj(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)

    marked1_color = models.CharField(max_length = 10,default='#dc143c',blank=True)
    marked1_w= models.FloatField(default=0.05)
    marked2_color = models.CharField(max_length = 10,default='#5feb4c',blank=True)
    marked2_w= models.IntegerField(default=1)
    marked3_color = models.CharField(max_length = 10,default='#eb4cc2',blank=True)
    marked3_w= models.IntegerField(default=1)

    week_color = models.CharField(max_length = 10,default='#bbe0e3',blank=True)
    week_s= models.FloatField(default=0.28)

    flag_head = models.BooleanField(default=True,blank=True)
    flag_footer = models.BooleanField(default=True,blank=True)
    flag_title = models.BooleanField(default=True,blank=True)
    flag_legend = models.BooleanField(default=True,blank=True)
    flag_logo = models.BooleanField(default=True,blank=True)
    flag_status_date= models.BooleanField(default=True,blank=True)

    title = models.CharField(max_length = 200,default='STATUS REPORT E/E',blank=True)
    created_by = models.CharField(max_length = 200,default='[EE-32]',blank=True)
    logo_url = models.CharField(max_length = 500,default="/static/brand/logos_seat_cupra.png",blank=True) #¿?

    #fig1_color_1 = models.CharField(max_length = 10,default='',blank=True) # to MPlan2
    #fig1_color_2 = models.CharField(max_length = 10,default='',blank=True) # to MPlan2
    #fig1_color_3 = models.CharField(max_length = 10,default='',blank=True) # to MPlan2
    #fig1_s= models.FloatField(default=0.28) # to MType_input2
    #fig1_border_w= models.IntegerField(default=1) # to MPlan2
    #fig1_name= models.CharField(max_length = 50,default='',blank=True) # to MType_input2

    #type_name= models.CharField(max_length = 50,default='',blank=True)
    #plan_name= models.CharField(max_length = 50,default='',blank=True)

    class Meta: # This class will let you force the name of the table to what you like.
        db_table = "Config_prj"

    def __str__(self):
        return '%s, %s' % (self.id, self.name)

    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])
class MProject(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length = 200,default='',blank=True)
    comment = models.CharField(max_length = 200,default='',blank=True)
    #variables representacion
    #Get day today
    today = date.today()
    d1 = today.strftime('%Y-%m-%d')

    date_ini = models.CharField(max_length = 50,default=d1,blank=True)
    date_end = models.CharField(max_length = 50,default=d1,blank=True)
    date_status = models.CharField(max_length = 50,default=d1,blank=True)
    max_ecu_slide = models.IntegerField(default=8,validators=[MinValueValidator(1), MaxValueValidator(100)])
    factor_weeks = models.IntegerField(default=1,validators=[MinValueValidator(1), MaxValueValidator(100)])

    class Meta: # This class will let you force the name of the table to what you like.
        db_table = "Project"

    def __str__(self):
        return '%s, %s' % (self.id, self.name)

    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])

class MVersion(models.Model):
    id = models.AutoField(primary_key=True)
    id_project = models.ForeignKey(to=MProject, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200,default='',blank=True)
    comment = models.CharField(max_length = 200,default='',blank=True)
    date = models.CharField(max_length = 50,default=datetime.today,blank=True)

    class Meta: # This class will let you force the name of the table to what you like.
        db_table = "Version"

    def __str__(self):
        #return self.name
        return '%s, %s' % (self.id, self.name)

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

class MECU(models.Model):
    id = models.AutoField(primary_key=True)
    id_version = models.ForeignKey(to=MVersion, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200,default='',blank=False, unique=False)
    dx_ecu = models.CharField(max_length = 50,default='',blank=True)
    comment = models.CharField(max_length = 200,default='',blank=True)
    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True) #user
    
    class Meta: # This class will let you force the name of the table to what you like.
        db_table = "ECU"

    def __str__(self):
        return '%s, %s' % (self.id, self.name)

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])


class MRelease_input(models.Model):
    id = models.AutoField(primary_key=True)
    #id_ecu = models.ForeignKey(to=MECU,  on_delete=models.CASCADE)
    id_ecu = models.ForeignKey(to=MECU,  on_delete=models.SET_NULL, null=True, blank=True)
    id_type_input = models.ForeignKey(to=MType_input2, on_delete=models.SET_NULL, null=True, blank=True) # pondrá en null el campo si el registro del ECU relacionado es eliminado de la base de datos

    n_version = models.CharField(max_length = 50,default='',blank=True)
    #date_beantragt = models.CharField(max_length = 50,default=datetime.today,blank=True)
    today = date.today()
    d1 = today.strftime("%d%m%Y")
    #date_beantragt = models.CharField(max_length = 50,default=datetime.now().strftime("%d%m%Y"), blank=True)
    date_beantragt = models.CharField(max_length = 50,default=d1, blank=True)
    
    #plan = models.CharField(max_length = 50,default='',blank=True)
    id_plan = models.ForeignKey(to=MPlan2, on_delete=models.SET_NULL, null=True, blank=True) # pondrá en null el campo si el registro del ECU relacionado es eliminado de la base de datos
    
    flag_visual = models.BooleanField(default=True,blank=True)
    #dx_ecu = models.CharField(max_length = 50,default='',blank=True)
    comment = models.CharField(max_length = 200,default='',blank=True)

    flag_marked1 = models.BooleanField(default=False,blank=True)
    flag_marked2 = models.BooleanField(default=False,blank=True)
    flag_marked3 = models.BooleanField(default=False,blank=True)

    created_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True) #user


    class Meta: # This class will let you force the name of the table to what you like.
        db_table = "Release_input"

    def __str__(self):
        return '%s, %s' % (self.id, self.name)

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])