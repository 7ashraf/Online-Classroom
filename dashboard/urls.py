from django.urls import path, include
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', dashboardRouter, name = 'dashboardRouter'),
    path('create-classroom/', createClassroom, name='create-classroom'),
    path('<str:classroomName>/', classroomRouter, name = 'classroomRouter' )
]