from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from trips.models import User, Product, UserProduct, Appointment
from trips.utilsModule import queries as tripQueries
from trips.utilsModule import modExceptions

def tripsModule(request, userId):
    if request.method == 'POST':
        try:
            productId = request.POST['productId']
            url = reverse('tripsTable', kwargs={'userId': userId, 'productId': productId})
            return redirect(url)
        except modExceptions.tripModuleError as e:
            return tripsTemplate(request, template, user, error=str(e))
    else:
        productsList = None
        selectedProduct = request.GET.get('productId', default=0)
        template = 'trips.html'
        try:
            user = tripQueries.getUserById(userId)
            productsList = tripQueries.getProducts()
            return tripsTemplate(request, template, user, selectedProduct=selectedProduct, productsList=productsList)
        except modExceptions.tripModuleError as e:
            return tripsTemplate(request, template, user, productsList=productsList, error=str(e))

def updateTrips(request, userId, productId):
    template = 'trips.html'
    try:
        user = tripQueries.getUserById(userId)
        productsList = tripQueries.getProducts()
        userProdList = tripQueries.userProductList(productId)
        return tripsTemplate(request, template, user, selectedProduct=productId, productsList=productsList, userProdList=userProdList)
    except modExceptions.tripModuleError as e:
        return tripsTemplate(request, template, user, productsList=productsList, error=str(e))

def usersTrips(request, userId, productId):
    template = 'tripsList.html'
    if request.method == 'POST':
        try:
            user = tripQueries.getUserById(userId)
            selectedUser = tripQueries.getUserById(request.POST['selectedUserId'])
            selectedProduct = tripQueries.getProductById(productId)
            userProdList = tripQueries.userProductList(productId)
            userList = tripQueries.getUsers()
            existingRecord = tripQueries.getUserProduct(selectedUser, productId)
            if existingRecord:
                raise modExceptions.tripModuleError('El usuario ya tiene asignado el producto')
            tripAssign = assignTrip(selectedUser, selectedProduct)
            tripQueries.saveUserProduct(tripAssign)
            return tripsTemplate(request, template, user, userList=userList, selectedProduct=selectedProduct, userProdList=userProdList)
        except modExceptions.tripModuleError as e:
            return tripsTemplate(request, template, user, userList=userList, selectedProduct=selectedProduct, userProdList=userProdList, error=str(e))
    else:
        try:
            user = tripQueries.getUserById(userId)
            productsList = tripQueries.getProducts()
            if productId == 0:
                raise modExceptions.tripModuleError('Seleccionar un producto para ver la lista de usuarios')
            selectedProduct = tripQueries.getProductById(productId)
            userProdList = tripQueries.userProductList(productId)
            userList = tripQueries.getUsers()
            return tripsTemplate(request, template, user, userList=userList, selectedProduct=selectedProduct, userProdList=userProdList)
        except modExceptions.tripModuleError as e:
            template = 'trips.html'
            return tripsTemplate(request, template, user, selectedProduct=productId, productsList=productsList, error=str(e))

def assignTrip(user, product):
    tripAssign = UserProduct()
    tripAssign.use_code = user
    tripAssign.pro_code = product    
    return tripAssign

def tripsTemplate(request, template, user, userList=None, selectedProduct=None, productsList=None, userProdList=None, error=None):    
    return render(request, template, {
            'user': user,
            'userList': userList,
            'selectedProduct': selectedProduct,
            'productsList': productsList,
            'userProdList': userProdList,
            'error': error
            })