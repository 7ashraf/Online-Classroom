from msilib.schema import Class
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from AuthApp.models import *
from dashboard.forms import CreateClassroomForm
# Create your views here.

def dashboardRouter(request):
    if request.user.is_student:
        return studentDashboard(request)
    else:
        return teacherDashboard(request)

def classroomRouter(request, classroomName):
    if request.user.is_student:
        return studentClassroom(request, classroomName)
    else:
        return teacherClassroom(request, classroomName)        


def studentDashboard(request):
    student = Student.objects.get(user = request.user) 
        
    if request.method == 'POST':
        classroomName = request.POST.get('name')
        student.classroom.add(Classroom.objects.get(name = classroomName))
    classrooms = Classroom.objects.filter(student = student)
    print(classrooms)
    ctx = {
        'classrooms' : classrooms
    }
    return render(request, 'student-dash.html', ctx)

def teacherDashboard(request):
    teacher = Teacher.objects.get(user = request.user)
    classrooms = Classroom.objects.filter(teacher = teacher)
    ctx = {
        'classrooms' : classrooms
    }
    return render(request, 'teacher-dash.html', ctx)
     
def createClassroom(request):
    if request.method == 'POST':

        form = CreateClassroomForm(request.POST)
        if form.is_valid :
            teacher = Teacher.objects.get(user = request.user)
            classroom = form.save(commit=False)
            classroom.teacher = teacher
            classroom.save()
            return redirect('/dashboard')
    else:
        form = CreateClassroomForm()
        return render(request, 'create-classroom.html', {
            'form':form
        })

def teacherClassroom(request, classroomName):
    classroom = Classroom.objects.get(name = classroomName)
    students = Student.objects.filter(classroom__name = classroomName)
    print(students)
    if request.method == 'POST':
        taskName = request.POST.get('taskName')
        task = Task(name = taskName, classroom = classroom)
        task.save()
    ctx = {
        'students' : students
    }

    return render(request, 'teacher-classroom.html', ctx)

def studentClassroom(request, classroomName):
    classroom = Classroom.objects.get(name = classroomName)
    user = request.user
    student = Student.objects.get(user = user)

    if request.method=='POST':
        taskName = request.POST.get('taskName')
        task = Task.objects.get( name = taskName)
        task.doneStudents.add(student)
        task.save()

    classroom = Classroom.objects.get(name = classroomName)
    tasks = Task.objects.filter(classroom = classroom)
    doneStudents = {}
    
    for task in tasks:
        doneStudents[task.name] = Student.objects.filter(task = task)
    print(doneStudents)

    for item  in doneStudents:
        if(student == doneStudents[item] ):
            print(f'Found {item} {doneStudents[item]}')
        else :
            print(student)
            print(doneStudents[item])
            print(False)
    ctx = {
        'tasks' : tasks,
        'user' : user,
        'student' : student,
        'doneStudents' : doneStudents
    }

    return render(request, 'student-classroom.html', ctx)