from django.urls import path

from . import views

app_name = 'log'
urlpatterns = [
    # ex: /polls/
    path('', views.login, name='login'),
    path('reg/', views.reg, name='reg'),
    path('log/', views.log, name='log'),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]