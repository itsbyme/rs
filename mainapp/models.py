from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from authapp.models import Teacher

# Create your models here.

class Parent(models.Model):
    id = models.AutoField(primary_key=True)
    surname = models.CharField(verbose_name="Фамилия", max_length=32)
    name = models.CharField(verbose_name="Имя", max_length=32)
    patronymic = models.CharField(verbose_name="Отчество", max_length=32, blank=True)
    phone = PhoneNumberField(verbose_name="Телефон", null=False, blank=False, unique=True, region='RU')
    email = models.EmailField(verbose_name="E-mail", max_length=128, unique = True)

    @property
    def get_full_name(self):
        return f'{self.surname} {self.name} {self.patronymic}'

    @property
    def get_students(self):
        return Student.objects.filter(pid=self.id)

    @property
    def get_payment_sum(self):
        return sum(payment.sum for payment in Payment.objects.filter(pid=self.id))

    def __str__(self):
        return f"{self.id} {self.get_full_name}"

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(verbose_name="Дата оплаты")
    sum = models.IntegerField(verbose_name="Сумма оплаты")
    comment = models.CharField(verbose_name="Комментарий", max_length=256)
    pid = models.ForeignKey(Parent, on_delete=models.CASCADE, verbose_name="Родитель")

    def __str__(self):
        pid = self.pid
        return f"{self.date} ({pid.surname} {pid.name} {pid.patronymic}) [{self.sum} рубасов]"

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    surname = models.CharField(verbose_name="Фамилия", max_length=32)
    name = models.CharField(verbose_name="Имя", max_length=32)
    patronymic = models.CharField(verbose_name="Отчество", max_length=32, blank=True)
    birthday = models.DateField(verbose_name="День рождения")
    pid = models.ForeignKey(Parent, on_delete=models.CASCADE, verbose_name="Родитель")

    @property
    def get_full_name(self):
        return f'{self.surname} {self.name} {self.patronymic}'

    @property
    def get_parents(self):
        return Parent.objects.filter(id=self.pid.id)

    @property
    def get_binds(self):
        return Bind.objects.filter(sid=self.id)

    @property
    def get_attendance(self):
        return Attendance.objects.filter(sid=self.id)

    def __str__(self):
        return f"{self.id} {self.get_full_name}"

class Time(models.Model):
    id = models.AutoField(primary_key=True)
    start = models.TimeField(verbose_name="Время начала занятия")
    end = models.TimeField(verbose_name='Время конца занятия')
    def __str__(self):
        return f'{self.start.strftime("%H:%M")}-{self.end.strftime("%H:%M")}'

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Название группы", max_length=16, unique=True)
    max_students = models.PositiveSmallIntegerField(
        verbose_name="Максимальное количество учеников", 
        default=8)
    day = models.PositiveSmallIntegerField(verbose_name='День')
    time = models.ForeignKey(Time, on_delete=models.CASCADE, verbose_name='Время проведения занятия')
    subject = models.CharField(verbose_name="Предмет", max_length=32)
    create_day = models.DateField(verbose_name='Дата создания')
    delete_day = models.DateField(verbose_name='Дата распада')
    tid = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Преподаватель')

    @property
    def get_binds(self):
        return Bind.objects.filter(gid=self.id)
    
    @property
    def get_teacher(self):
        return Teacher.objects.get(id=self.tid.id)

    @property
    def get_dates(self):
        return Date.objects.filter(gid=self.id)

    @property
    def get_list_dates(self):
        return list(i.date for i in self.get_dates)
    
    @property
    def get_attendance(self):
        return (Attendance.objects.filter(did=i) for i in Date.objects.filter(gid=self.id))

    @property
    def get_day(self):
        days = {
            1: "Пн",
            2: "Вт",
            3: "Ср",
            4: "Чт",
            5: "Пт",
            6: "Сб",
        }
        return days[self.day]

    @property
    def get_shedule(self):
        return f'{self.time} {self.get_day}'

    def __str__(self):
        return f"{self.id} {self.name}"

class Bind(models.Model):
    id = models.AutoField(primary_key=True)
    sid = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Ученик")
    gid = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа")

    @property
    def get_student(self):
        return Student.objects.get(id=self.sid.id)
    
    @property
    def get_group(self):
        return Group.objects.get(id=self.gid.id)

    def __str__(self):
        return f"{self.get_group.name} {self.get_student.get_full_name}"

class Date(models.Model):
    id = models.AutoField(primary_key=True)
    gid = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
    date = models.DateField(verbose_name='Дата проведения занятия')
    status = models.BooleanField(verbose_name='Занятие проведено')
    
    def __str__(self):
        return f'{self.gid.name} {self.date}'

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    did = models.ForeignKey(Date, on_delete=models.CASCADE, verbose_name="Дата")
    status = models.BooleanField(verbose_name="Посещение")
    sid = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Ученик')

    def __str__(self):
        return f'{self.sid.get_full_name} {self.did.gid.name}'
