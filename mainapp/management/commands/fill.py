from django.core.management.base import BaseCommand

import json
import os

from mainapp import models
from authapp.models import Teacher

JSON_PATH = 'data/json'

def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as file:
        return json.load(file)

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        teachers = load_from_json('teachers')
        parents = load_from_json('parents')
        groups = load_from_json('groups')
        payments = load_from_json('payments')
        students = load_from_json('students')
        binds = load_from_json('binds')
        dates = load_from_json('dates')
        attendances = load_from_json('attendances')
        times = load_from_json('times')
        

        print("Adding....")

        Teacher.objects.all().delete()
        print('....Teachers')
        for teacher in teachers:
            Teacher.objects.create_user(**teacher).save()

        models.Parent.objects.all().delete()
        print('....Parents')
        for parent in parents:
            models.Parent(**parent).save()

        models.Time.objects.all().delete()
        print('....Times')
        for time in times:
            models.Time(**time).save()

        models.Group.objects.all().delete()
        print('....Groups')
        for group in groups:
            group['time'] = models.Time.objects.all()[group['time'] - 1]
            group['tid'] = models.Teacher.objects.all()[group['tid'] - 1]
            models.Group(**group).save()

        models.Student.objects.all().delete()
        print('....Students')
        for student in students:
            student['pid'] = models.Parent.objects.all()[student['pid'] - 1]
            models.Student(**student).save()

        models.Bind.objects.all().delete()
        print('....Binds')
        for bind in binds:
            bind['sid'] = models.Student.objects.all()[bind['sid'] - 1]
            bind['gid'] = models.Group.objects.all()[bind['gid'] - 1]
            models.Bind(**bind).save()

        models.Date.objects.all().delete()
        print('....Dates')
        for date in dates:
            date['gid'] = models.Group.objects.all()[date['gid'] - 1]
            models.Date(**date).save()

        models.Attendance.objects.all().delete()
        print('....Attendances')
        for attendance in attendances:
            attendance['did'] = models.Date.objects.all()[attendance['did'] - 1]
            attendance['sid'] = models.Student.objects.all()[attendance['sid'] - 1]
            models.Attendance(**attendance).save()

        models.Payment.objects.all().delete()
        print('....Payments')
        for payment in payments:
            payment['pid'] = models.Parent.objects.all()[payment['pid'] - 1]
            models.Payment(**payment).save()

        print("Creating admin")
        Teacher.objects.create_superuser(username='deffer00@yandex.ru', password='password', surname='Шаталов', name='Максим', patronymic='Игоревич', phone='88888')