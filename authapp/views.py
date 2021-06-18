from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import TeacherLoginForm
from django.contrib import auth
from django.urls import reverse

# Create your views here.

def login(request):
    form = TeacherLoginForm(data=request.POST)
    if request.method == 'POST' and form.is_valid():
        email = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=email, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('mainapp:home'))

    
    content = {'login_form': form}
    return render(request, 'mainapp/index.html', content)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')