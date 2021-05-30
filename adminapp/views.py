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
    pass

def group_update(request, pk):
    edit_group = get_object_or_404(models.Group, pk=pk)
    if request.method == 'POST':
        edit_form = forms.GroupForm(request.POST, request.FILES,
                                            instance=edit_group)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:group_update',
                                                args=[edit_group.pk]))
    else:
        edit_form = forms.GroupForm(instance=edit_group)

    context = {
        'update_form': edit_form,
        'pk': pk,
    }

    return render(request, 'adminapp/group_update.html', context)

def group_delete(request, pk):
    get_object_or_404(models.Group, pk=pk).delete()
    return HttpResponseRedirect(reverse('admin:groups'))

def students(request):
    context = {
        'students': models.Student.objects.all(),
    }
    return render(request, 'adminapp/students.html', context)

def student_create(request):
    pass

def student_update(request, pk):
    edit_student = get_object_or_404(models.Student, pk=pk)
    if request.method == 'POST':
        edit_form = forms.StudentForm(request.POST, request.FILES,
                                            instance=edit_student)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:student_update',
                                                args=[edit_student.pk]))
    else:
        edit_form = forms.StudentForm(instance=edit_student)

    context = {
        'update_form': edit_form,
        'pk': pk,
    }

    return render(request, 'adminapp/student_update.html', context)

def student_delete(request, pk):
    get_object_or_404(models.Student, pk=pk).delete()
    return HttpResponseRedirect(reverse('admin:students'))

def parents(request):
    context = {
        'parents': models.Parent.objects.all(),
    }
    return render(request, 'adminapp/parents.html', context)

def parent_create(request):
    pass

def parent_update(request, pk):
    edit_parent = get_object_or_404(models.Parent, pk=pk)
    if request.method == 'POST':
        edit_form = forms.ParentForm(request.POST, request.FILES,
                                            instance=edit_parent)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:parent_update',
                                                args=[edit_parent.pk]))
    else:
        edit_form = forms.ParentForm(instance=edit_parent)

    context = {
        'update_form': edit_form,
        'pk': pk,
    }

    return render(request, 'adminapp/parent_update.html', context)

def parent_delete(request, pk):
    get_object_or_404(models.Parent, pk=pk).delete()
    return HttpResponseRedirect(reverse('admin:parents'))

def teachers(request):
    context = {
        'teachers': models.Teacher.objects.all(),
    }
    return render(request, 'adminapp/teachers.html', context)

def teacher_create(request):
    pass

def teacher_update(request, pk):
    edit_teacher = get_object_or_404(models.Teacher, pk=pk)
    if request.method == 'POST':
        edit_form = forms.TeacherForm(request.POST, request.FILES,
                                            instance=edit_teacher)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:teacher_update',
                                                args=[edit_teacher.pk]))
    else:
        edit_form = forms.TeacherForm(instance=edit_teacher)

    context = {
        'update_form': edit_form,
        'pk': pk,
    }

    return render(request, 'adminapp/teacher_update.html', context)

def teacher_delete(request, pk):
    get_object_or_404(models.Teacher, pk=pk).delete()
    return HttpResponseRedirect(reverse('admin:teachers'))

