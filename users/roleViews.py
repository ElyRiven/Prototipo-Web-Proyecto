from django.shortcuts import render, redirect
from users.models import User, Role
from users.authentication import utils, authExceptions
from users.utilsModule import queries, modExceptions
from django.urls import reverse
from django.db import IntegrityError

def rolesModule(request, userId):
    if request.method == 'POST':
        pass
    else:
        try:        
            user = queries.getUserById(userId)
            rolesList = queries.getRoles()
            return render(request, 'roles.html', {
                'user': user,
                'rolesList': rolesList,
                'module': 'Roles',
                'title': 'Listado de Roles',
                'buttonAddRole': 'Agregar Rol'
                })
        except modExceptions.roleModuleError:
            return render(request, 'roles.html', {
                'user': user,
                'error': 'Error al cargar el módulo de roles',
                'module': 'Roles',
                'title': 'Listado de Roles'})

def addRole(request, userId):
    if request.method == 'POST':
        roleName = request.POST['roleName'].upper()
        newRole = Role()
        newRole.rol_name = roleName
        try:            
            queries.saveNewRole(newRole)
            url = reverse('roles', kwargs={'userId': userId})
            return redirect(url)
        except modExceptions.roleModuleError:
            return render(request, 'rolesAdd.html', {
                'user': user,
                'error': 'Error al guardar el nuevo rol',
                'module': 'Roles',
                'title': 'Nuevo Rol'})
    else:
        try:
            user = queries.getUserById(userId)
            return render(request, 'rolesAdd.html', {
                'user': user,                
                'module': 'Roles',
                'title': 'Nuevo Rol',
                })
        except modExceptions.roleModuleError:
            return render(request, 'rolesAdd.html', {
                'user': user,
                'error': 'Error al cargar el módulo de roles',
                'module': 'Roles',
                'title': 'Nuevo Rol'})

def editRole(request, userId, roleId):
    if request.method == 'POST':
        updatedRole = request.POST['roleName'].upper()
        try:
            queries.updateRole(roleId, updatedRole)
            url = reverse('roles', kwargs={'userId': userId})
            return redirect(url)
        except modExceptions.roleModuleError:
            return render(request, 'rolesUpdate.html', {
                'user': user,
                'error': 'Error al guardar el nuevo rol',
                'module': 'Roles',
                'title': 'Actualizar Rol'})
    else:
        try:
            user = queries.getUserById(userId)
            role = queries.getRoleById(roleId)
            return render(request, 'rolesUpdate.html', {
                'user': user,
                'role': role,
                'module': 'Roles',
                'title': 'Actualizar Rol'
                })
        except modExceptions.roleModuleError:
            return render(request, 'rolesUpdate.html', {
                'user': user,
                'error': 'Error al cargar la interfaz de edición de roles',
                'module': 'Roles',
                'title': 'Actualizar Rol'})

def deleteRole(request, userId, roleId):    
    try:
        user = queries.getUserById(userId)
        queries.deleteRole(roleId)
        url = reverse('roles', kwargs={'userId': userId})
        return redirect(url)
    except IntegrityError:
        rolesList = queries.getRoles()
        return render(request, 'roles.html', {
            'user': user,
            'rolesList': rolesList,
            'error': 'No se puede borrar el registro. Existen usuarios asignados a este rol',
            'module': 'Roles',
            'title': 'Listado de Roles',
            'buttonAddRole': 'Agregar Rol'
            })