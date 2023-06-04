from .views import *
from django.urls import path

app_name = 'AuthApp'
urlpatterns = [
    path('', home), 
    path('login/', log_in, name = 'login'),
    path('logout/', log_out, name = 'logout'),
    path('register/', register)
]