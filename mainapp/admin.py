from django.contrib import admin

from . import models
from authapp.models import Teacher
# Register your models here.

models = (
    Teacher,
    models.Parent, 
    models.Payment, 
    models.Student, 
    models.Group, 
    models.Bind, 
    models.Attendance,
    models.Date
)

for model in models:
    admin.site.register(model)
