from argparse import ONE_OR_MORE
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError('email missing')
        if not username:
            raise ValueError('username missing')
        user = self.model(
            email = self.normalize_email(email),
            username = username, 
            **other_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user


    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        user = self.model(
            email = self.normalize_email(email),
            password = password,
            username = username
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        (1,'Teacher'),
        (2,'Student'),
    )
    email               = models.EmailField (verbose_name = 'email' ,max_length=254, unique=True)
    username            = models.CharField(verbose_name = 'username',max_length=254, null=True, blank=True)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    is_admin            = models.BooleanField(default=False)
    last_login          = models.DateTimeField(null=True, blank=True)
    date_joined         = models.DateTimeField(auto_now_add=True)
    is_student          = models.BooleanField(default=False)
    is_teacher          = models.BooleanField(default=False)
    #user_type = models.CharField(blank=False, choices=USER_TYPE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True



class Teacher(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.user.email


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    #students = models.ManyToManyField(Student, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def addTask(self, taskName):
        pass

    def __str__(self):
        return self.name
    
class Student(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    classroom = models.ManyToManyField(Classroom)

    def __str__(self):
        return self.user.email




class Task(models.Model):
    name = models.CharField(max_length=100, default='task')

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    doneStudents = models.ManyToManyField(Student)

    def __str__(self):
        return self.name