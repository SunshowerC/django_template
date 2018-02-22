from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
from project.common.decorator import post_method, get_method

from django import forms
from .models import User

import logging
logger = logging.getLogger('root')

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=50)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')


def reg(request):
	return render(request, 'register.html' )

def log(request):
	return render(request, 'login.html' )


'''API'''
@post_method
def login(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.filter(username__exact=username,password__exact=password)

        if user:
            return render(request, 'index.html',{'userform':user})
        else:
            return HttpResponse('用户名或密码错误,请重新登录')

    else:
        userform = UserForm()
    return HttpResponse(userform)



@post_method
def register(request):
    if request.method == 'POST':
    	
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            email = userform.cleaned_data['email']

            user = User(username=username,password=password,email=email)
            user.save()

            return HttpResponse('regist success!!!')
    else:
        userform = UserForm()

    return JsonResponse({'userform':userform});






