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
        selectedProduct = None
        template = 'trips.html'
        try:
            user = tripQueries.getUserById(userId)
            productsList = tripQueries.getProducts()
            selectedProduct = request.GET.get('productId')
            return tripsTemplate(request, template, user, selectedProduct=selectedProduct, productsList=productsList)
        except modExceptions.tripModuleError as e:
            return tripsTemplate(request, template, user, productsList=productsList, error=str(e))

def updateTrips(request, userId, productId):
    template = 'tripsTable.html'
    try:
        user = tripQueries.getUserById(userId)
        productsList = tripQueries.getProducts()
        userProdList = tripQueries.userProductList(productId)
        return tripsTemplate(request, template, user, selectedProduct=productId, productsList=productsList, userProdList=userProdList)
    except modExceptions.tripModuleError as e:
        return tripsTemplate(request, template, user, productsList=productsList, error=str(e))

def tripsTemplate(request, template, user, selectedProduct=None, productsList=None, userProdList=None, error=None):    
    return render(request, template, {
            'user': user,
            'selectedProduct': selectedProduct,
            'productsList': productsList,
            'userProdList': userProdList,
            'error': error
            })