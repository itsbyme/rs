from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms import widgets

import datetime

from . import models

# Create your views here.

def go_to_login(request):
    return HttpResponseRedirect('login/')

@login_required
def home(request):
    return HttpResponseRedirect(reverse('mainapp:shedule'))

@login_required
def parents(request):
    groups = map(lambda x: x.get_binds,
            models.Group.objects.filter(tid=request.user.id))
    students = set(map(lambda bind: bind.get_student,
        (bind for binds in groups for bind in binds)))
    parents = set(map(lambda student: student.pid, 
        students))

    context = {
        'parents': parents
    }
    return render(request, 'mainapp/parents.html', context)

@login_required
def students(request):
    groups = map(lambda x: x.get_binds,
            models.Group.objects.filter(tid=request.user.id))
    students = set(map(lambda bind: bind.get_student, 
            (bind for binds in groups for bind in binds)))

    context = {
            'students': students,
    }
    return render(request, 'mainapp/students.html', context)

@login_required
def groups(request):
    context = {
        'groups': models.Group.objects.filter(tid=request.user.id),
    }
    return render(request, 'mainapp/groups.html', context)

@login_required
def parent(request, pk):
    parent = get_object_or_404(models.Parent, pk=pk)
    context = {
        'parent': parent,
        'payments': models.Payment.objects.filter(pid=parent.id)
    }
    return render(request, 'mainapp/parent.html', context)

@login_required
def group(request, pk):
    group = get_object_or_404(models.Group, pk=pk)
    return render(request, 'mainapp/group.html', {'group': group})

@login_required
def student(request, pk):
    student = get_object_or_404(models.Student, pk=pk)
    return render(request, 'mainapp/student.html', {'student': student})

@login_required
def salary(request):
    states = sorted([i for i in request.user.get_dates 
        if i[0].date.month == datetime.datetime.today().month],
        key=lambda x: x[0].date)
    total = sum(i[0].status for i in states) * 1000
    return render(request, 'mainapp/salary.html', {'states': states, 'total': total})

@login_required
def shedule(request):
    class State:
        def __init__(self):
            self.state = False
        
        @property
        def true(self):
            self.state = True
            return ''
        
        @property
        def false(self):
            self.state = False
            return ''
        
        def __bool__(self):
            return self.state

    today = datetime.datetime.today()
    week = [today + datetime.timedelta(days=i) for i in range(7)]
    week = [datetime.date(i.year, i.month, i.day) for i in week]
    context = {
        'week': [(i.strftime('%d.%m, %a'), i) for i in week],
        'times': models.Time.objects.all(),
        'groups': models.Group.objects.filter(tid=request.user.id),
        'state': State(),
    }
    return render(request, 'mainapp/shedule.html', context)

@login_required
def marks(request):
    today = datetime.datetime.today()
    time = datetime.time(today.hour, today.minute)
    time = models.Time.objects.filter(start__lte=time, end__gte=time)
    time = time.first() if time else None
    group = None

    context = {
        'state': 0,
    }
    if request.method == 'POST':
        form = type('Form', (forms.BaseForm,), request.POST)
        if form.is_valid:
            group = models.Group.objects.get(tid=request.user.id, day=today.isoweekday(), time=time.id)
            date = models.Date.objects.get(gid=group.id, date=datetime.date(today.year, today.month, today.day))
            date.status = True
            date.save()
            good = set()
            for key in request.POST:
                if not key.startswith('status_'):
                    continue
                key = int(key.replace('status_', ''))
                good.add(key)
            bad = set(i.sid.id for i in models.Bind.objects.filter(gid=group)) - good
            for i in good:
                student = models.Student.objects.get(id=i)
                attendance = models.Attendance.objects.filter(did=date,
                                                        status=False,
                                                        sid=student).first()
                if not attendance:
                    continue
                models.Payment(date=today, 
                        sum=-1000, 
                        comment=f'Оплата за {student.get_full_name}', 
                        pid=student.pid).save()
                attendance.status = True
                attendance.save()
            for i in bad:
                student = models.Student.objects.get(id=i)
                attendance = models.Attendance.objects.filter(did=date,
                                                        status=True,
                                                        sid=student).first()
                if not attendance:
                    continue
                models.Payment(date=today, 
                        sum=1000, 
                        comment=f'Возврат за {student.get_full_name}', 
                        pid=student.pid).save()
                attendance.status = False
                attendance.save()
            
        return render(request, 'mainapp/start.html')
    else:
        if time:
            group = models.Group.objects.filter(tid=request.user.id,
                    day=today.isoweekday(), time=time.id).first()
            if group:
                form = type('Form', (forms.BaseForm,), {'base_fields': {}})
                date = models.Date.objects.get(gid=group, date=today)
                for bind in group.get_binds:
                    initial = models.Attendance.objects.get(sid=bind.sid,
                                                            did=date).status
                    form.base_fields[f'status_{bind.sid.id}'] = forms.BooleanField(required=False, 
                                                                                initial=initial,
                                                                                label=bind.sid.get_full_name)
                    if bind.sid.pid.get_payment_sum < 1000:
                        form.base_fields[f'status_{bind.sid.id}'].disabled = True
                
                context['state'] = 1
                context['form'] = form

        if not (time and group):
            groups = models.Group.objects.filter(tid=request.user.id)
            date = min((j for i in groups for j in models.Date.objects.filter(gid=i.id) 
                        if j.date >= datetime.date.today()), key=lambda x: x.date)
            context['date'] = date
            context['group'] = models.Group.objects.get(id=date.gid.id)
    return render(request, 'mainapp/marks.html', context)
