from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from mainapp import models as mainapp

# Create your models here.

class Teacher(AbstractUser):
    id = models.AutoField(primary_key=True)
    surname = models.CharField(verbose_name="Фамилия", max_length=32)
    name = models.CharField(verbose_name="Имя", max_length=32)
    patronymic = models.CharField(verbose_name="Отчество", blank=True, max_length=32)
    phone = PhoneNumberField(verbose_name="Телефон", null=False, blank=False, unique=True, region='RU', error_messages={
                                                                                                        'invalid': 'Введите корректный номер, например: +7 999 123-45-67',
                                                                                                        'reqiered': 'Это поле обязательно!'
    })

    @property
    def get_full_name(self):
        return f'{self.surname} {self.name} {self.patronymic}'

    @property
    def get_dates(self):
        return ((date, group) for group in mainapp.Group.objects.filter(tid=self.id) for date in group.get_dates)
        
    def __str__(self):
        return f'{self.id} {self.get_full_name}'
