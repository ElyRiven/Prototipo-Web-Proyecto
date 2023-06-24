from django.urls import reverse
from django.shortcuts import render, redirect
from products.utilsModule import modExceptions
from products.utilsModule import queries as placeQueries
from products.models import User, Product, Place
from datetime import datetime

def placeModule(request, userId, productId):
    placesList = None
    template = 'places.html'
    try:
        user = placeQueries.getUserById(userId)
        product = placeQueries.getProductById(productId)
        placesList = placeQueries.getPlaceByProductId(productId)
        return placeTemplate(request, template, user, product=product, placesList=placesList)
    except modExceptions.placeModuleError as e:
        return placeTemplate(request, template, user, placesList, error=str(e))

def addPlace(request, userId, productId):
    template = 'placesAdd.html'
    if request.method == 'POST':
        try:
            user = placeQueries.getUserById(userId)
            product = placeQueries.getProductById(productId)
            newPlace = Place()
            startDate = datetime.strptime(request.POST['placeStartDate'], '%Y-%m-%d').date()
            endDate = datetime.strptime(request.POST['placeEndDate'], '%Y-%m-%d').date()
            if endDate <= startDate:
                raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
            newPlace = assignPlace(newPlace,
                                    request.POST['placeName'].upper(),
                                    request.POST['placeDescription'].upper(),
                                    request.POST['placeActivity'].upper(),
                                    request.POST['placeCity'].upper(),
                                    startDate,
                                    endDate,
                                    product)
            placeQueries.savePlace(newPlace)
            url = reverse('places', kwargs={'userId': userId, 'productId': productId})
            return redirect(url)
        except ValueError as e:
            return placeTemplate(request, template, user, error=str(e))
        except modExceptions.placeModuleError as e:
            return placeTemplate(request, template, user, error=str(e))
    else:
        try:
            user = placeQueries.getUserById(userId)
            product = placeQueries.getProductById(productId)
            return placeTemplate(request, template, user, product=product)
        except modExceptions.placeModuleError as e:
            return placeTemplate(request, template, user, error=str(e))

def editPlace(request, userId, productId, placeId):
    template = 'placesUpdate.html'
    if request.method == 'POST':
        try:
            user = placeQueries.getUserById(userId)
            product = placeQueries.getProductById(productId)
            editedPlace = placeQueries.getPlaceById(placeId)
            startDate = datetime.strptime(request.POST['placeStartDate'], '%Y-%m-%d').date()
            endDate = datetime.strptime(request.POST['placeEndDate'], '%Y-%m-%d').date()
            if endDate <= startDate:
                raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
            editedPlace = assignPlace(editedPlace,
                                    request.POST['placeName'].upper(),
                                    request.POST['placeDescription'].upper(),
                                    request.POST['placeActivity'].upper(),
                                    request.POST['placeCity'].upper(),
                                    startDate,
                                    endDate,
                                    product)
            placeQueries.savePlace(editedPlace)
            url = reverse('places', kwargs={'userId': userId, 'productId': productId})
            return redirect(url)
        except ValueError as e:
            return placeTemplate(request, template, user, error=str(e))
        except modExceptions.placeModuleError as e:
            return placeTemplate(request, template, user, error=str(e))
    else:
        try:
            user = placeQueries.getUserById(userId)
            product = placeQueries.getProductById(productId)
            place = placeQueries.getPlaceById(placeId)
            return placeTemplate(request, template, user, product=product, place=place)
        except modExceptions.placeModuleError as e:
            return placeTemplate(request, template, user, error=str(e))

def deletePlace(request, userId, productId, placeId):
    template = 'places.html'
    try:
        user = placeQueries.getUserById(userId)
        product = placeQueries.getProductById(productId)
        placeQueries.deletePlace(placeId)
        url = reverse('places', kwargs={'userId': userId, 'productId': productId})
        return redirect(url)
    except modExceptions.placeModuleError as e:
        return placeTemplate(request, template, user, product=product, error=str(e))

def assignPlace(place, plaName, plaDescription, plaActivity, plaCity, placeStartDate, placeEndDate, product):
    place.pla_name = plaName
    place.pla_description = plaDescription
    place.pla_activity = plaActivity
    place.pla_city = plaCity
    place.pla_startdate = placeStartDate
    place.pla_enddate = placeEndDate
    place.pro_code = product
    return place

def placeTemplate(request, template, user, product=None, placesList=None, place=None, error=None):    
    return render(request, template, {
            'user': user,
            'product': product,
            'placesList': placesList,
            'place': place,
            'error': error
            })