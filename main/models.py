from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class student(models.Model):
	first_name = models.CharField(max_length = 20)
	last_name = models.CharField(max_length = 20)
	b_date = models.DateField('Birth Date')
	roll = models.CharField(max_length = 20, primary_key=True)
	dept = models.CharField(max_length = 20)
	batch  = models.CharField(max_length = 21)

'''
class teacher(models.Model):
	name = models.CharField(max_length = 20)
	dept = models.CharField(max_length = 20)
	subject = models.CharField(max_length = 20)
'''

class CustomUser(AbstractUser):
    pass
    dept = models.CharField(max_length = 20)
    userRole = models.CharField(max_length = 20)
    # add additional fields in here



class EnrollCourse(models.Model):
	teacher = models.CharField(max_length = 20)
	session = models.CharField(max_length = 20)
	dept = models.CharField(max_length = 20)
	batch  = models.CharField(max_length = 20)