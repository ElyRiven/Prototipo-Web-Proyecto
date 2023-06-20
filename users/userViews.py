from django.shortcuts import render, redirect
from users.models import User, Role
from users.authentication import utils, authExceptions
from users.utilsModule import queries, modExceptions
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

def addUser(request, userId):
    if request.method == 'POST':
        newUser = User()
        newUser.use_firstname = request.POST['userFirstName'].upper()
        newUser.use_lastname = request.POST['userLastName'].upper()
        newUser.use_email = request.POST['userEmail'].upper()
        newUser.use_idnumber = request.POST['userIdNumber']
        newUser.use_phonenumber = request.POST['userPhone']

        #Get Role by Id
        roleAssing = request.POST['userRole']
        role = queries.getRoleById(roleAssing)
        newUser.rol_code = role

        #Encrypt password Here
        password = utils.encryptPassword(request.POST['userPassword'])
        newUser.use_password = password
        try:
            queries.saveUser(newUser)
            queries.addBenefitToUser(newUser)
            url = reverse('users', kwargs={'userId': userId})
            return redirect(url)
        except modExceptions.userModuleError:
            return render(request, 'usersAdd.html', {
                'user': user,
                'error': 'Error al guardar el nuevo usuario',
                'module': 'Usuarios',
                'title': 'Nuevo Usuario'})
    else:
        try:
            user = queries.getUserById(userId)
            rolesList = queries.getRoles()
            return render(request, 'usersAdd.html', {
                'user': user,
                'rolesList': rolesList,
                'module': 'Usuarios',
                'title': 'Nuevo Usuario',
                })
        except modExceptions.userModuleError:
            return render(request, 'usersAdd.html', {
                'user': user,
                'error': 'Error al cargar la interfaz de añadir usuario',
                'module': 'Usuarios',
                'title': 'Nuevo Usuario'})

def editUser(request, userId, userToEditId):
    if request.method == 'POST':
        user = queries.getUserById(userToEditId)
        user.use_firstname = request.POST['userFirstName'].upper()
        user.use_lastname = request.POST['userLastName'].upper()
        user.use_email = request.POST['userEmail'].upper()
        user.use_idnumber = request.POST['userIdNumber']
        user.use_phonenumber = request.POST['userPhone']
        user.use_points = request.POST['userPoints']

        #Get Role by Id
        roleAssing = request.POST['userRole']
        role = queries.getRoleById(roleAssing)
        user.rol_code = role

        try:
            queries.saveUser(user)
            url = reverse('users', kwargs={'userId': userId})
            return redirect(url)
        except modExceptions.userModuleError:
            return render(request, 'usersUpdate.html', {
                'user': user,
                'error': 'Error al guardar los cambios',
                'module': 'Usuarios',
                'title': 'Editar Usuario'})
    else:
        try:
            user = queries.getUserById(userId)
            rolesList = queries.getRoles()
            userToEdit = queries.getUserById(userToEditId)
            return render(request, 'usersUpdate.html', {
                'user': user,
                'userToEdit': userToEdit,
                'rolesList': rolesList,
                'module': 'Usuarios',
                'title': 'Editar Usuario',
                })
        except modExceptions.userModuleError:
            return render(request, 'usersUpdate.html', {
                'user': user,
                'error': 'Error al cargar la interfaz de editar usuario',
                'module': 'Usuarios',
                'title': 'Editar Usuario'})

def deleteUser(request, userId, userToDeleteId):    
    try:
        user = queries.getUserById(userId)
        if userId == userToDeleteId:
            usersList = queries.getUsers()
            return render(request, 'users.html', {
                'user': user,
                'usersList': usersList,
                'error': 'No se puede eliminar el usuario con el que se ha inciado sesión',
                'module': 'Usuarios',
                'title': 'Listado de Usuarios',
                'buttonAddUser': 'Agregar Usuario',
                'buttonManageRoles': 'Administrar Roles'
                })
        queries.deleteUser(userToDeleteId)
        url = reverse('users', kwargs={'userId': userId})
        return redirect(url)
    except modExceptions.userModuleError:
        return render(request, 'users.html', {
            'user': user,
            'error': 'Error al eliminar el usuario',
            'module': 'Usuarios',
            'title': 'Listado de Usuarios'})