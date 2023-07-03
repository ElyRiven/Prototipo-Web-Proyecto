from django.shortcuts import render, redirect
from users.models import User, Role
from users.authentication import utils, authExceptions
from users.utilsModule import queries, modExceptions
from django.urls import reverse
from datetime import datetime

def login(request):
    template = 'login.html'
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
                        raise authExceptions.userLoginError('Usuario no autorizado')
                else:
                    raise authExceptions.userLoginError('Contraseña Incorrecta')
            else:
                raise authExceptions.userLoginError('Usuario Incorrecto')
        except authExceptions.userLoginError as e:
            return usersTemplate(request, template, error=str(e))
    else:
        return render(request, template)

def usersModule(request, userId):
    template = 'users.html'
    try:
        user = queries.getUserById(userId)
        usersList = queries.getUsers()
        return usersTemplate(request, template, user=user, usersList=usersList)
    except modExceptions.userModuleError as e:
        return usersTemplate(request, template, user=user, error=str(e))

def addUser(request, userId):
    template = 'usersAdd.html'
    if request.method == 'POST':
        newUser = User()
        #Get Role by Id
        roleAssing = request.POST['userRole']
        role = queries.getRoleById(roleAssing)
        #Encrypt password Here
        password = utils.encryptPassword(request.POST['userPassword'])
        newUser = assignUser(newUser,
                                request.POST['userFirstName'].upper(),
                                request.POST['userLastName'].upper(),
                                request.POST['userEmail'].upper(),
                                request.POST['userIdNumber'],
                                request.POST['userPhone'],
                                role,
                                password
                             )
        try:
            queries.saveUser(newUser)
            queries.addBenefitToUser(newUser)
            url = reverse('users', kwargs={'userId': userId})
            return redirect(url)
        except modExceptions.userModuleError as e:
            return usersTemplate(request, template, user=user, error=str(e))
    else:
        try:
            user = queries.getUserById(userId)
            rolesList = queries.getRoles()
            return usersTemplate(request, template, user=user, rolesList=rolesList)
        except modExceptions.userModuleError as e:
            return usersTemplate(request, template, user=user, rolesList=rolesList, error=str(e))

def editUser(request, userId, userToEditId):
    template = 'usersUpdate.html'
    if request.method == 'POST':
        user = queries.getUserById(userToEditId)
        #Update the first login Date
        newFirstLoginDate = datetime.strptime(request.POST['userFirstLogin'], '%Y-%m-%d').date()

        #Get Role by Id
        roleAssing = request.POST['userRole']
        role = queries.getRoleById(roleAssing)

        user = assignUser(user,
                                request.POST['userFirstName'].upper(),
                                request.POST['userLastName'].upper(),
                                request.POST['userEmail'].upper(),
                                request.POST['userIdNumber'],
                                request.POST['userPhone'],
                                role,
                                points=request.POST['userPoints'],
                                firstLogin=request.POST['userFirstLogin']
                             )
        try:
            queries.saveUser(user)
            url = reverse('users', kwargs={'userId': userId})
            return redirect(url)
        except modExceptions.userModuleError as e:
            return usersTemplate(request, template, user=user, error=str(e))
    else:
        try:
            user = queries.getUserById(userId)
            rolesList = queries.getRoles()
            userToEdit = queries.getUserById(userToEditId)
            return usersTemplate(request, template, user=user, rolesList=rolesList, userToEdit=userToEdit)
        except modExceptions.userModuleError as e:
            return usersTemplate(request, template, user=user, rolesList=rolesList, userToEdit=userToEdit, error=str(e))

def deleteUser(request, userId, userToDeleteId):
    template = 'users.html'    
    try:
        user = queries.getUserById(userId)
        usersList = queries.getUsers()
        if userId == userToDeleteId:
            raise modExceptions.userModuleError('No se puede eliminar el usuario con el que se ha inciado sesión')
        queries.deleteUser(userToDeleteId)
        url = reverse('users', kwargs={'userId': userId})
        return redirect(url)
    except modExceptions.userModuleError as e:
        return usersTemplate(request, template, user=user, usersList=usersList, error=str(e))

def assignUser(user, firstName, lastName, email, idNumber, phone, role, password=None, points=None, firstLogin=None):
    user.use_firstname = firstName.upper()
    user.use_lastname = lastName.upper()
    user.use_email = email.upper()
    user.use_idnumber = idNumber
    user.use_phonenumber = phone
    if password is not None:
        user.use_password = password
    if points is not None:
        user.use_points = points
    if firstLogin is not None:
        user.use_firstlogin = firstLogin
    user.rol_code = role
    return user

def usersTemplate(request, template, user=None, usersList=None, rolesList=None, userToEdit=None, error=None):
    return render(request, template, {
            'user': user,
            'usersList': usersList,
            'rolesList': rolesList,
            'userToEdit': userToEdit,
            'error': error
            })