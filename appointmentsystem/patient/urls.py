"""
URL configuration for appointmentsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from patient import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('alldoctor', views.alldoctor, name='alldoctor'),
    path('register', views.register, name='register'),
    path('register_check', views.register_check, name='register_check'),
    path('login_check', views.login_check, name='login_check'),
    path('login', views.login, name='login'),
    path('appointment/<int:id>', views.appointment, name='appointment'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout, name='logout'),
    path('book_appointment', views.book_appointment, name='book_appointment'),
    path('payment', views.payment, name='payment'),
    path('payment_success', views.payment_success, name='payment_success'),
    path('contact_check', views.contact_check, name='contact_check'),
    path('feedback/<int:id>', views.feedback, name='feedback'),
    path('feedback_check', views.feedback_check, name='feedback_check'),
    path('cancel_appointment/<int:id>', views.cancel_appointment, name='cancel_appointment'),


]



