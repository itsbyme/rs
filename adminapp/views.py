from datetime import datetime, timedelta
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse

from mainapp import models
from . import forms
from django import forms as djforms

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
            create_day = datetime.strptime(form.data['create_day'], "%Y-%m-%d").date()
            delete_day = datetime.strptime(form.data['delete_day'], "%Y-%m-%d").date()
            group = form.save()
            delta = delete_day - create_day
            for day in range (delta.days + 1):
                date = create_day + timedelta(days=day)
                if date.isoweekday() == group.day:
                    models.Date(gid=group, date=date, status=False).save()
            
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
    students = (bind.get_student for bind in group.get_binds)
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
        'students': students,
        'form': form,
        'pk': pk,
    }

    return render(request, 'adminapp/group.html', context)

def group_delete(request, pk):
    get_object_or_404(models.Group, pk=pk).delete()
    return HttpResponseRedirect(reverse('admin:groups'))

def add_students_to_group(request, pk):
    group = get_object_or_404(models.Group, pk=pk)
    context = {
        'group': group,
    }
    if request.method == 'POST':
        form = type('Form', (djforms.BaseForm,), request.POST)
        if form.is_valid:
            add = set()
            remove = set()
            for key in request.POST:
                if not key.startswith('student_'):
                    continue
                key = int(key.replace('student_', ''))
                add.add(key)
            
            if len(add) > group.max_students:
                return HttpResponseRedirect(reverse('admin:add_students_to_group', args=[group.id]))

            remove = set(bind.sid.id for bind in models.Bind.objects.filter(gid=group)) - add
            
            for pk in add:
                student = get_object_or_404(models.Student, pk=pk)
                if not models.Bind.objects.filter(sid=student, gid=group):
                    models.Bind(sid=student, gid=group).save()

                    for date in group.get_dates:
                        models.Attendance(did=date, sid=student, status=False).save()
            
            for pk in remove:
                student = get_object_or_404(models.Student, pk=pk)
                models.Bind.objects.get(sid=student, gid=group).delete()
            
            return HttpResponseRedirect(reverse('admin:group_update', args=[group.id]))
    else:
        form = type('Form', (djforms.BaseForm,), {'base_fields': {}})
        for student in models.Student.objects.all():
            initial = True if models.Bind.objects.filter(sid=student.id, gid=group.id) else False
            form.base_fields[f'student_{student.id}'] = djforms.BooleanField(required=False, 
                                                                            initial=initial,
                                                                            label=student.get_full_name)
            context['form'] = form

    return render(request, 'adminapp/add_students_to_group.html', context)


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
    groups = (bind.get_group for bind in student.get_binds)
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
        'groups': groups,
        'form': form,
        'pk': pk,
    }

    return render(request, 'adminapp/student.html', context)

def student_delete(request, pk):
    get_object_or_404(models.Student, pk=pk).delete()
    return HttpResponseRedirect(reverse('admin:students'))

def add_groups_to_student(request, pk):
    student = get_object_or_404(models.Student, pk=pk)
    context = {
        'student': student,
    }
    if request.method == 'POST':
        form = type('Form', (djforms.BaseForm,), request.POST)
        if form.is_valid:
            add = set()
            remove = set()
            for key in request.POST:
                if not key.startswith('group_'):
                    continue
                key = int(key.replace('group_', ''))
                add.add(key)
            for pk in add:
                group = models.Group.objects.get(pk=pk)
                print(group.max_students, len(group.get_binds))
                if group.max_students < len(group.get_binds) + 1:
                    return HttpResponseRedirect(reverse('admin:add_groups_to_student', args=[student.id]))

            remove = set(bind.gid.id for bind in models.Bind.objects.filter(sid=student)) - add
            
            for pk in add:
                group = get_object_or_404(models.Group, pk=pk)
                if not models.Bind.objects.filter(sid=student, gid=group):
                    models.Bind(sid=student, gid=group).save()
                    for date in group.get_dates:
                        models.Attendance(did=date, sid=student, status=False).save()
            
            for pk in remove:
                group = get_object_or_404(models.Group, pk=pk)
                models.Bind.objects.get(sid=student, gid=group).delete()
            return HttpResponseRedirect(reverse('admin:student_update', args=[student.id]))
    else:
        form = type('Form', (djforms.BaseForm,), {'base_fields': {}})
        for group in models.Group.objects.all():
            initial = True if models.Bind.objects.filter(sid=student.id, gid=group.id) else False
            form.base_fields[f'group_{group.id}'] = djforms.BooleanField(required=False, 
                                                                            initial=initial,
                                                                            label=f'{ group.name }({ len(group.get_binds) }/{ group.max_students })')
            context['form'] = form

    return render(request, 'adminapp/add_groups_to_student.html', context)

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
                                            instance=parent)
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

