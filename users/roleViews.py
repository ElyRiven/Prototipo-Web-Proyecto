from django.shortcuts import render, redirect
from users.models import User, Role
from users.authentication import utils, authExceptions
from users.utilsModule import queries, modExceptions
from django.urls import reverse

def rolesModule(request, userId):
    template = 'roles.html'
    try:
        user = queries.getUserById(userId)
        rolesList = queries.getRoles()
        return rolesTemplate(request, template, user, rolesList=rolesList)
    except modExceptions.roleModuleError as e:
        return rolesTemplate(request, template, user, error=str(e))

def addRole(request, userId):
    template = 'rolesAdd.html'
    if request.method == 'POST':
        roleName = request.POST['roleName'].upper()
        newRole = Role()
        newRole.rol_name = roleName
        try:
            user = queries.getUserById(userId)
            queries.saveNewRole(newRole)
            url = reverse('roles', kwargs={'userId': userId})
            return redirect(url)
        except modExceptions.roleModuleError as e:
            return rolesTemplate(request, template, user, error=str(e))
    else:
        try:
            user = queries.getUserById(userId)
            return rolesTemplate(request, template, user)
        except modExceptions.roleModuleError as e:
            return rolesTemplate(request, template, user, error=str(e))

def editRole(request, userId, roleId):
    template = 'rolesUpdate.html'
    if request.method == 'POST':
        updatedRole = request.POST['roleName'].upper()
        try:
            user = queries.getUserById(userId)
            queries.updateRole(roleId, updatedRole)
            url = reverse('roles', kwargs={'userId': userId})
            return redirect(url)
        except modExceptions.roleModuleError as e:
            return rolesTemplate(request, template, user, error=str(e))
    else:
        try:
            user = queries.getUserById(userId)
            role = queries.getRoleById(roleId)
            return rolesTemplate(request, template, user, role=role)
        except modExceptions.roleModuleError as e:
            return rolesTemplate(request, template, user, error=str(e))

def deleteRole(request, userId, roleId):
    template = 'roles.html'
    try:
        user = queries.getUserById(userId)
        queries.deleteRole(roleId)
        url = reverse('roles', kwargs={'userId': userId})
        return redirect(url)
    except modExceptions.roleModuleError as e:
        rolesList = queries.getRoles()
        return rolesTemplate(request, template, user, rolesList=rolesList, error=str(e))

def rolesTemplate(request, template, user, rolesList=None, role=None, error=None):    
    return render(request, template, {
            'user': user,
            'rolesList': rolesList,
            'role': role,
            'error': error
            })