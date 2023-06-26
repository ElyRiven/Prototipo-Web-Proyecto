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
from products import productViews, placeViews
from trips import tripViews

urlpatterns = [
    path('', lambda request: redirect('login/')),
    # Login URL
    path('login/', userViews.login, name='login'),
    # Users URLs
    path('users/<int:userId>/', userViews.usersModule, name='users'),
    path('users/<int:userId>/newUser/', userViews.addUser, name='newUser'),
    path('users/<int:userId>/updateUser/<int:userToEditId>/', userViews.editUser, name='updateUser'),
    path('users/<int:userId>/deleteUser/<int:userToDeleteId>/', userViews.deleteUser, name='deleteUser'),
    # Roles URLs
    path('users/<int:userId>/roles/', roleViews.rolesModule, name='roles'),
    path('users/<int:userId>/newRole/', roleViews.addRole, name='newRole'),
    path('users/<int:userId>/updateRole/<int:roleId>/', roleViews.editRole, name='updateRole'),
    path('users/<int:userId>/deleteRole/<int:roleId>/', roleViews.deleteRole, name='deleteRole'),
    # Products URLs
    path('products/<int:userId>/', productViews.productsModule, name='products'),
    path('products/<int:userId>/newProduct/', productViews.addProduct, name='newProduct'),
    path('products/<int:userId>/updateProduct/<int:productId>', productViews.editProduct, name='updateProduct'),
    path('products/<int:userId>/deleteProduct/<int:productId>', productViews.deleteProduct, name='deleteProduct'),
    # Places URLs
    path('products/<int:userId>/places/<int:productId>/', placeViews.placeModule, name='places'),
    path('products/<int:userId>/newPlace/<int:productId>/', placeViews.addPlace, name='newPlace'),
    path('products/<int:userId>/updatePlace/<int:productId>/<int:placeId>/', placeViews.editPlace, name='updatePlace'),
    path('products/<int:userId>/deletePlace/<int:productId>/<int:placeId>/', placeViews.deletePlace, name='deletePlace'),
    # Trips URLs
    path('trips/<int:userId>/', tripViews.tripsModule, name='trips'),
    path('trips/<int:userId>/product/<int:productId>/', tripViews.updateTrips, name='tripsTable'),
    path('trips/<int:userId>/product/<int:productId>/userList/', tripViews.usersTrips, name='tripsUsersList'),
    path('trips/<int:userId>/product/<int:productId>/appointment/<int:selectedUserId>/', tripViews.appointmentModule, name='appointments'),
    path('trips/<int:userId>/product/<int:productId>/activate/', tripViews.activateTrips, name='activateTrips'),
]
