from django.urls import path

from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.go_to_login),
    path('home/', views.home, name='home'),
    # path('parents/', views.parents, name='parents'),
    path('students/', views.students, name='students'),
    path('groups/', views.groups, name='groups'),
    path('parent/<int:pk>/', views.parent, name='parent'),
    path('group/<int:pk>/', views.group, name='group'),
    path('student/<int:pk>/', views.student, name='student'),
    path('salary/', views.salary, name='salary'),
    path('shedule/', views.shedule, name='shedule'),
    path('marks/', views.marks, name='marks'),
]
