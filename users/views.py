from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from users.models import User, Role
from users.authentication import utils, authExceptions
from users.userModule import queries, modExceptions
from django.urls import reverse

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = utils.getUserByEmail(email)
            if user:
                if utils.checkPassword(user, password):
                    if utils.checkRole(user):
                        userId = user.use_code
                        url = reverse('users', kwargs={'userId': userId})
                        return redirect(url)
                    else:
                        return render(request, 'login.html', {'error': 'Usuario no autorizado'})
                else:
                    return render(request, 'login.html', {'error': 'Contraseña Incorrecta'})
            else:
                return render(request, 'login.html', {'error': 'Usuario Incorrecto'})
        except authExceptions.userLoginError:
            return render(request, 'login.html', {'error': 'Error al iniciar sesión'})
    else:
        return render(request, 'login.html')

def usersModule(request, userId):
    try:
        user = queries.getUserById(userId)
        usersList = queries.getUsers()
        return render(request, 'users.html', {
            'user': user,
            'usersList': usersList,
            'module': 'Usuarios',
            'title': 'Listado de Usuarios',
            'buttonAddUser': 'Agregar Usuario',
            'buttonManageRoles': 'Administrar Roles',
            })
    except modExceptions.userModuleError:        
        return render(request, 'users.html', {
            'user': user,
            'error': 'Error al cargar el módulo de usuarios',
            'module': 'Usuarios',
            'title': 'Listado de Usuarios'})

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

def rolesModuleAddRole(request, userId):
    if request.method == 'POST':
        newRole = request.POST['roleName'].upper()
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

def rolesModuleEditRole(request, userId, roleId):
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

def rolesModuleDeleteRole(request, userId, roleId):    
    try:
        user = queries.getUserById(userId)
        queries.deleteRole(roleId)
        url = reverse('roles', kwargs={'userId': userId})
        return redirect(url)
    except modExceptions.roleModuleError:            
        return render(request, 'roles.html', {
            'user': user,
            'error': 'Error al eliminar el rol',
            'module': 'Roles',
            'title': 'Listado de Roles'})