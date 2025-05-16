from django.contrib import admin
from django.urls import path
from fir import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('fir/submit/', views.submit_fir, name='submit_fir'),
    path('firs/', views.view_firs, name='view_firs'),  # NEW,
    path('fir_form/', views.fir, name='fir_form'),  # NEW,
    path('login/', views.login, name='login'),  # NEW,
]


