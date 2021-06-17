from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

from mainapp.models import Student, Group, Parent, Teacher

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
    
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''
            field.widget.attrs['class'] = 'form-control'
            
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'create_day': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'delete_day': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'day': forms.Select(choices=[(1, 'Пн'),
                                        (2, 'Вт'),
                                        (3, 'Ср'),
                                        (4, 'Чт'),
                                        (5, 'Пт'),
                                        (6, 'Сб'),
            ]),
        }
    
    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''
            field.widget.attrs['class'] = 'form-control'

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(ParentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''
            field.widget.attrs['class'] = 'form-control'

class TeacherForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = fields = ('surname', 'name', 'patronymic', 'phone', 'username')
        widgets = {
            'username': forms.EmailInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'
        for field_name, field in self.fields.items():
            field.help_text = ''
            field.widget.attrs['class'] = 'form-control col-lg-4'
