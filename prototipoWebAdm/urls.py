"""
URL configuration for prototipoWebAdm project.

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
from django.urls import path
from django.shortcuts import redirect
from users import views

urlpatterns = [
    path('', lambda request: redirect('login/')),
    path('login/', views.login, name='login'),
    path('users/<int:userId>/', views.usersModule, name='users'),
    path('users/<int:userId>/roles/', views.rolesModule, name='roles'),
    path('users/<int:userId>/roles/newRole/', views.rolesModuleAddRole, name='newRole'),
    path('users/<int:userId>/roles/updateRole/<int:roleId>/', views.rolesModuleEditRole, name='updateRole'),
    path('users/<int:userId>/roles/deleteRole/<int:roleId>/', views.rolesModuleDeleteRole, name='deleteRole')
]
