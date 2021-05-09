from django import forms
from django.contrib.auth.forms import AuthenticationForm
from authapp.models import Teacher

class TeacherLoginForm(AuthenticationForm):
    class Meta:
        model = Teacher
        fields = ('username', 'password')
    
    def __init__(self, *args, **kwargs):
        super(TeacherLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'
        self.fields['username'].widget.attrs['placeholder'] = 'Еmail'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'
        for field_name, field in self.fields.items():
            field.help_text = ''
            field.widget.attrs['class'] = 'form-control col-lg-4'
            field.default_error_messages = {'required': ''}
            
