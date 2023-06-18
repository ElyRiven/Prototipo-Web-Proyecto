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