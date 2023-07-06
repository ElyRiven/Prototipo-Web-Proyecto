from django.http import HttpResponse, HttpResponseNotFound
from api.models import User, Role
from api.utilsModule import modExceptions
from api.utilsModule import queries as apiQueries
from django.core import serializers
from datetime import datetime
from django.middleware import csrf
import json

def verifyUser(request):
    if request.method == 'GET':
        username = request.GET.get('username').upper()
        password = request.GET.get('password')
        try:
            user = apiQueries.validateUser(username, password)
            if user is not None:
                userJson = serializers.serialize('json', [user])
                response = HttpResponse(userJson, content_type='application/json')
                response['X-CSRFToken'] = csrf.get_token(request)
                return response
            else:
                return HttpResponseNotFound()
        except modExceptions.apiException as e:
            return HttpResponseNotFound(e)

def apiUser(request):
    if request.method == 'GET':
        userId = request.GET.get('userId')
        try:
            user = apiQueries.getUserById(userId)
            if user is not None:
                userJson = serializers.serialize('json', [user])
                response = HttpResponse(userJson, content_type='application/json')
                response['X-CSRFToken'] = csrf.get_token(request)
                return response
            else:
                return HttpResponseNotFound()
        except modExceptions.apiException as e:
            return HttpResponseNotFound(e)
        
    elif request.method == 'PUT':
        data = json.loads(request.body)
        userId = data.get('use_code')
        firstName = data.get('use_firstname').upper()
        lastName = data.get('use_lastname').upper()
        mail = data.get('use_email').upper()
        idNumber = data.get('use_idnumber')
        phone = data.get('use_phonenumber')
        if data.get('use_password') is not '':
            password = apiQueries.encryptPassword(data.get('use_password'))
        else:
            password = None
        points = data.get('use_points')
        section = data.get('use_bensection')
        firstLogin = datetime.strptime(data.get('use_firstlogin'), '%Y-%m-%d').date()
        role = data.get('rol_code')
        try:
            userToEdit = apiQueries.getUserById(userId)
            getRole = apiQueries.getRoleById(role)
            userToEdit = assignUser(userToEdit,
                                    firstName, 
                                    lastName, 
                                    mail, 
                                    idNumber, 
                                    phone, 
                                    getRole, 
                                    section,
                                    password=password,
                                    points=points, 
                                    firstLogin=firstLogin)
            if apiQueries.saveUser(userToEdit):
                return HttpResponse('Usuario actualizado correctamente')
        except modExceptions.apiException as e:
            return HttpResponse(e)

def assignUser(user, firstName, lastName, email, idNumber, phone, role, section, password=None, points=None, firstLogin=None):
    user.use_firstname = firstName.upper()
    user.use_lastname = lastName.upper()
    user.use_email = email.upper()
    user.use_idnumber = idNumber
    user.use_phonenumber = phone
    user.rol_code = role
    user.use_bensection = section
    if password is not None:
        user.use_password = password
    if points is not None:
        user.use_points = points
    if firstLogin is not None:
        user.use_firstlogin = firstLogin
    return user