from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse

from mainapp import models
from . import forms

# Create your views here.

def index(request):
    return render(request, 'adminapp/index.html')

def groups(request):
    context = {
        'groups': models.Group.objects.all(),
    }
    return render(request, 'adminapp/groups.html', context)

def group_create(request):
    if request.method == 'POST':
        form = forms.GroupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:groups'))
    else:
        form = forms.GroupForm()

    context = {
        'upd': False,
        'form': form
    }

    return render(request, 'adminapp/group.html', context)

def group_update(request, pk):
    group = get_object_or_404(models.Group, pk=pk)
    if request.method == 'POST':
        form = forms.GroupForm(request.POST, request.FILES,
                                            instance=group)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:group_update',
                                                args=[group.pk]))
    else:
        form = forms.GroupForm(instance=group)

    context = {
        'upd': True,
        'form': form,
        'pk': pk,
    }

    return render(request, 'adminapp/group.html', context)

def group_delete(request, pk):
    get_object_or_404(models.Group, pk=pk).delete()
    return HttpResponseRedirect(reverse('admin:groups'))

def students(request):
    context = {
        'students': models.Student.objects.all(),
    }
    return render(request, 'adminapp/students.html', context)

def student_create(request):
    if request.method == 'POST':
        form = forms.StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:student_update'))
    else:
        form = forms.StudentForm()

    context = {
        'upd': False,
        'form': form
    }

    return render(request, 'adminapp/student.html', context)

def student_update(request, pk):
    student = get_object_or_404(models.Student, pk=pk)
    if request.method == 'POST':
        form = forms.StudentForm(request.POST, request.FILES,
                                            instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:student_update',
                                                args=[student.pk]))
    else:
        form = forms.StudentForm(instance=student)

    context = {
        'upd': True,
        'form': form,
        'pk': pk,
    }

    return render(request, 'adminapp/student.html', context)

def student_delete(request, pk):
    get_object_or_404(models.Student, pk=pk).delete()
    return HttpResponseRedirect(reverse('admin:students'))

def parents(request):
    context = {
        'parents': models.Parent.objects.all(),
    }
    return render(request, 'adminapp/parents.html', context)

def parent_create(request):
    if request.method == 'POST':
        form = forms.ParentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:parents'))
    else:
        form = forms.ParentForm()
    
    context = {
        'upd': False,
        'form': form,
    }

    return render(request, 'adminapp/parent.html', context)

def parent_update(request, pk):
    parent = get_object_or_404(models.Parent, pk=pk)
    if request.method == 'POST':
        form = forms.ParentForm(request.POST, request.FILES,
                                            instance=edit_parent)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:parent_update',
                                                args=[parent.pk]))
    else:
        form = forms.ParentForm(instance=parent)

    context = {
        'upd': True,
        'form': form,
        'pk': pk,
    }

    return render(request, 'adminapp/parent.html', context)

def parent_delete(request, pk):
    get_object_or_404(models.Parent, pk=pk).delete()
    return HttpResponseRedirect(reverse('admin:parents'))

def teachers(request):
    context = {
        'teachers': models.Teacher.objects.all(),
    }
    return render(request, 'adminapp/teachers.html', context)

def teacher_create(request):
    if request.method == 'POST':
        form = forms.TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:teachers'))
    else:
        form = forms.TeacherForm()

    context = {
        'upd': False,
        'form': form,
    }

    return render(request, 'adminapp/teacher.html', context)

def teacher_update(request, pk):
    teacher = get_object_or_404(models.Teacher, pk=pk)
    if request.method == 'POST':
        form = forms.TeacherForm(request.POST, request.FILES,
                                            instance=teacher)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:teacher_update',
                                                args=[teacher.pk]))
    else:
        form = forms.TeacherForm(instance=teacher)

    context = {
        'upd': True,
        'form': form,
        'pk': pk,
    }

    return render(request, 'adminapp/teacher.html', context)

def teacher_delete(request, pk):
    get_object_or_404(models.Teacher, pk=pk).delete()
    return HttpResponseRedirect(reverse('admin:teachers'))

