from django.urls import path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),
    path('groups/', adminapp.groups, name='groups'),
    path('groups/create/', adminapp.group_create, name='group_create'),
    path('groups/update/<int:pk>', adminapp.group_update, name='group_update'),
    path('groups/delete/<int:pk>', adminapp.group_delete, name='group_delete'),
    path('students/', adminapp.students, name='students'),
    path('students/create/', adminapp.student_create, name='student_create'),
    path('students/update/<int:pk>', adminapp.student_update, name='student_update'),
    path('students/delete/<int:pk>', adminapp.student_delete, name='student_delete'),
    path('parents/', adminapp.parents, name='parents'),
    path('parents/create/', adminapp.parent_create, name='parent_create'),
    path('parents/update/<int:pk>', adminapp.parent_update, name='parent_update'),
    path('parents/delete/<int:pk>', adminapp.parent_delete, name='parent_delete'),
    path('teachers/', adminapp.teachers, name='teachers'),
    path('teachers/create/', adminapp.teacher_create, name='teacher_create'),
    path('teachers/update/<int:pk>', adminapp.teacher_update, name='teacher_update'),
    path('teachers/delete/<int:pk>', adminapp.teacher_delete, name='teacher_delete'),
]

