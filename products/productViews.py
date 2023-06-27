from django.urls import reverse
from django.shortcuts import render, redirect
from products.utilsModule import queries as productQueries
from products.utilsModule import modExceptions
from products.models import User, Product
from datetime import datetime

def productsModule(request, userId):
    productsList = None
    template = 'products.html'
    try:
        user = productQueries.getUserById(userId)
        productsList = productQueries.getProducts()
        return productsTemplate(request, template, user, productsList)
    except modExceptions.productModuleError as e:
        return productsTemplate(request, template, user, productsList, error=str(e))

def addProduct(request, userId):
    template = 'productsAdd.html'
    if request.method == 'POST':
        try:
            user = productQueries.getUserById(userId)
            newProduct = Product()
            # Validate Dates
            startDate = datetime.strptime(request.POST['productStartDate'], '%Y-%m-%d').date()
            endDate = datetime.strptime(request.POST['productEndDate'], '%Y-%m-%d').date()
            if endDate <= startDate:
                raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
            # Validate Price
            price = checkPrice(request.POST['productPrice'])
            newProduct = assignProduct(newProduct, 
                                        request.POST['productName'].upper(),
                                        price,
                                        request.POST['productDescription'].upper(),
                                        request.POST['productCountry'].upper(),
                                        startDate,
                                        endDate)
            productQueries.saveProduct(newProduct)
            url = reverse('products', kwargs={'userId': userId})
            return redirect(url)
        except ValueError as e:
            return productsTemplate(request, template, user, error=str(e))
        except modExceptions.productModuleError as e:
            return productsTemplate(request, template, user, error=str(e))
    else:
        try:
            user = productQueries.getUserById(userId)
            return productsTemplate(request, template, user)
        except modExceptions.productModuleError as e:
            return productsTemplate(request, template, user, error=str(e))

def editProduct(request, userId, productId):
    template = 'productsUpdate.html'
    if request.method == 'POST':
        try:
            user = productQueries.getUserById(userId)
            product = productQueries.getProductById(productId)
            startDate = datetime.strptime(request.POST['productStartDate'], '%Y-%m-%d').date()
            endDate = datetime.strptime(request.POST['productEndDate'], '%Y-%m-%d').date()
            if endDate <= startDate:
                raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
            price = checkPrice(request.POST['productPrice'])
            editedProduct = assignProduct(product,
                                            request.POST['productName'].upper(),
                                            price,
                                            request.POST['productDescription'].upper(),
                                            request.POST['productCountry'].upper(),
                                            startDate,
                                            endDate,
                                            request.POST['productState'].upper())
            productQueries.saveProduct(editedProduct)
            url = reverse('products', kwargs={'userId': userId})
            return redirect(url)
        except ValueError as e:
            return productsTemplate(request, template, user, error=str(e))
        except modExceptions.productModuleError as e:
            return productsTemplate(request, template, user, error=str(e))
    else:
        try:
            user = productQueries.getUserById(userId)
            product = productQueries.getProductById(productId)
            return productsTemplate(request, template, user, product=product)
            pass
        except modExceptions.productModuleError as e:
            return productsTemplate(request, template, user, error=str(e))

def deleteProduct(request, userId, productId):
    template = 'products.html'
    try:
        user = productQueries.getUserById(userId)
        productsList = productQueries.getProducts()
        productQueries.deleteProduct(productId)
        url = reverse('products', kwargs={'userId': userId})
        return redirect(url)
    except modExceptions.productModuleError as e:
            return productsTemplate(request, template, user, productsList, error=str(e))

def checkPrice(price):
    priceCheck = price.replace(',', '.')
    if not validateFloatPrice(priceCheck):
        raise ValueError('El precio debe ser numérico y separado por punto')
    priceCheck = float(priceCheck)
    if priceCheck <= 0:
        raise ValueError('El precio debe ser mayor a 0')
    if len(str(priceCheck).split('.')[1]) > 2:
        raise ValueError('El precio debe tener máximo 2 decimales')
    return priceCheck
   
def validateFloatPrice(price):
    try:
        float(price)
        return True
    except ValueError:
        return False

def assignProduct(product, prodName, prodPrice, prodDescription, prodCountry, prodStartDate, prodEndDate , prodState=None):
    product.pro_name = prodName
    product.pro_price = prodPrice
    product.pro_description = prodDescription
    product.pro_country = prodCountry
    product.pro_startdate = prodStartDate
    product.pro_enddate = prodEndDate
    if prodState is not None:
        product.pro_state = prodState
    return product

def productsTemplate(request, template, user, productsList=None, product=None, error=None):    
    return render(request, template, {
            'user': user,
            'productsList': productsList,
            'product': product,
            'error': error
            })