from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
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

def apiGetUsers(request):
    if request.method == 'GET':
        try:
            usersList = apiQueries.getAllUsers()
            if usersList is not None:
                usersJson = serializers.serialize('json', usersList)
                response = HttpResponse(usersJson, content_type='application/json')
                return response
            else:
                HttpResponseNotFound()
        except modExceptions.apiException as e:
            return HttpResponseNotFound(e)

def apiGetBenefits(request):
    if request.method == 'GET':
        try:
            benefitsList = apiQueries.getAllBenefits()
            if benefitsList is not None:
                benefitsJson = serializers.serialize('json', benefitsList)
                response = HttpResponse(benefitsJson, content_type='application/json')
                return response
            else:
                HttpResponseNotFound()
        except modExceptions.apiException as e:
            return HttpResponseNotFound(e)

def apiCheckTrip(request):
    if request.method == 'GET':
        userId = request.GET.get('userId')
        try:
            userCheck = apiQueries.getUserProductByUserId(userId)
            if userCheck is not None:
                userCheckJson = serializers.serialize('json', [userCheck])
                response = HttpResponse(userCheckJson, content_type='application/json')
                return response                
            else:
                return HttpResponseNotFound()
        except modExceptions.apiException as e:
            return HttpResponseNotFound(e)

def apiGetProduct(request):
    if request.method == 'GET':
        productId = request.GET.get('productId')
        try:
            product = apiQueries.getProductById(productId)
            if product is not None:
                productJson = serializers.serialize('json', [product])
                response = HttpResponse(productJson, content_type='application/json')
                return response
            else:
                return HttpResponseNotFound()
        except modExceptions.apiException as e:
            return HttpResponseNotFound(e)

def apiGetQuestions(request):
    if request.method == 'GET':
        country = request.GET.get('country').upper()
        try:
            countryDB = apiQueries.getCountryByName(country)
            questionsList = apiQueries.getAllQuestionByCountryId(countryDB.cou_code)
            if questionsList is not None:
                questionsJson = serializers.serialize('json', questionsList)
                response = HttpResponse(questionsJson, content_type='application/json')
                return response
            else:
                HttpResponseNotFound()
        except modExceptions.apiException as e:
            return HttpResponseNotFound(e)

def apiSavePoints(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        userId = data.get('use_code')
        points = data.get('use_points')
        try:
            userToEdit = apiQueries.getUserById(userId)
            userToEdit.use_points += points
            if apiQueries.saveUser(userToEdit):
                return HttpResponse('Puntos actualizados correctamente')
            else:
                return HttpResponseNotFound()
        except modExceptions.apiException as e:
            return HttpResponse(e)

def apiGetUserBenefits(request):
    if request.method == 'GET':
        userId = request.GET.get('userId')
        try:
            userBenefitsList = apiQueries.getAllUserBenefitByUserId(userId)
            if userBenefitsList is not None:
                userBenefitsJson = serializers.serialize('json', userBenefitsList)
                response = HttpResponse(userBenefitsJson, content_type='application/json')
                return response
            else:
                return HttpResponseNotFound()
        except modExceptions.apiException as e:
            return HttpResponse(e)

def apiCompleteBenefit(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        userId = data.get('use_code')
        benefitId = data.get('ben_code')
        try:
            benefitToEdit = apiQueries.getUserBenefit(userId, benefitId)
            benefitToEdit.useben_state = "COMPLETE"
            if apiQueries.saveUserBenefit(benefitToEdit):
                return HttpResponse('Beneficio Completado correctamente')
            else:
                return HttpResponseNotFound()
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