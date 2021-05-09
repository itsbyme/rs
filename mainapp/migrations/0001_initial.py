# Generated by Django 3.0.4 on 2020-06-15 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('surname', models.CharField(max_length=32, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=32, verbose_name='Имя')),
                ('patronymic', models.CharField(blank=True, max_length=32, verbose_name='Отчество')),
                ('phone', models.CharField(max_length=16, verbose_name='Телефон')),
                ('email', models.CharField(max_length=32, unique=True, verbose_name='E-mail')),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start', models.TimeField(verbose_name='Время начала занятия')),
                ('end', models.TimeField(verbose_name='Время конца занятия')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('surname', models.CharField(max_length=32, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=32, verbose_name='Имя')),
                ('patronymic', models.CharField(blank=True, max_length=32, verbose_name='Отчество')),
                ('birthday', models.DateField(verbose_name='День рождения')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Parent', verbose_name='Родитель')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(verbose_name='Дата оплаты')),
                ('sum', models.IntegerField(verbose_name='Сумма оплаты')),
                ('comment', models.CharField(max_length=256, verbose_name='Комментарий')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Parent', verbose_name='Родитель')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='Название группы')),
                ('max_students', models.PositiveSmallIntegerField(default=8, verbose_name='Максимальное количество учеников')),
                ('day', models.PositiveSmallIntegerField(verbose_name='День')),
                ('subject', models.CharField(max_length=32, verbose_name='Предмет')),
                ('create', models.DateField(verbose_name='Дата создания')),
                ('delete', models.DateField(verbose_name='Дата распада')),
                ('tid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Преподаватель')),
                ('time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Time', verbose_name='Время проведения занятия')),
            ],
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(verbose_name='Дата проведения занятия')),
                ('status', models.BooleanField(verbose_name='Занятие проведено')),
                ('gid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Group', verbose_name='Группа')),
            ],
        ),
        migrations.CreateModel(
            name='Bind',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('gid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Group', verbose_name='Группа')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Student', verbose_name='Ученик')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(verbose_name='Посещение')),
                ('did', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Date', verbose_name='Дата')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Student', verbose_name='Ученик')),
            ],
        ),
    ]