from django.contrib import admin
from AuthApp.models import *
# Register your models here.
admin.site.register(MyUser)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Classroom)
admin.site.register(Task)