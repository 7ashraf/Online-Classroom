from msilib.schema import Class
from django import forms
from django.forms import ModelForm
from AuthApp.models import *

class CreateClassroomForm(ModelForm):
    class Meta:
        model = Classroom
        exclude = ['teacher']
        meta = ['name']
