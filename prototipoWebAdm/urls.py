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
from users import roleViews, userViews
from products import productViews

urlpatterns = [
    path('', lambda request: redirect('login/')),
    # Login URL
    path('login/', userViews.login, name='login'),
    # Users URLs
    path('users/<int:userId>/', userViews.usersModule, name='users'),
    path('users/<int:userId>/users/newUser/', userViews.addUser, name='newUser'),
    path('users/<int:userId>/users/updateUser/<int:userToEditId>/', userViews.editUser, name='updateUser'),
    path('users/<int:userId>/users/deleteUser/<int:userToDeleteId>/', userViews.deleteUser, name='deleteUser'),
    # Roles URLs
    path('users/<int:userId>/roles/', roleViews.rolesModule, name='roles'),
    path('users/<int:userId>/roles/newRole/', roleViews.addRole, name='newRole'),
    path('users/<int:userId>/roles/updateRole/<int:roleId>/', roleViews.editRole, name='updateRole'),
    path('users/<int:userId>/roles/deleteRole/<int:roleId>/', roleViews.deleteRole, name='deleteRole'),
    # Products URLs
    path('products/<int:userId>/', productViews.productsModule, name='products')
]
