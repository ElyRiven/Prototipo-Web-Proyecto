from django.shortcuts import render
from users.utilsModule import queries as userQueries
from products.utilsModule import queries as productQueries
from products.utilsModule import modExceptions
from products.models import User, Product, Place
from datetime import datetime

def productsModule(request, userId):
    productsList = None
    template = 'products.html'
    try:
        user = userQueries.getUserById(userId)
        productsList = productQueries.getProducts()
        return productsTemplate(request, template, user, productsList)
    except modExceptions.productModuleError as e:
        errorMessage = str(e)
        return productsTemplate(request, template, user, productsList, errorMessage)

def addProduct(request, userId):
    template = 'productsAdd.html'
    if request.method == 'POST':
        newProduct = Product()
        newProduct.pro_name = request.POST['productName'].upper()
        newProduct.pro_description = request.POST['productDescription'].upper()
        newProduct.pro_country = request.POST['productCountry'].upper()

        startDate = request.POST['productStartDate']
        endDate = request.POST['productEndDate']

        startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
        endDate = datetime.strptime(endDate, '%Y-%m-%d').date()

        # Check Price & Dates
        try:
            user = userQueries.getUserById(userId)
            # Validate Dates
            if endDate <= startDate:
                raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
            newProduct.pro_startdate = startDate
            newProduct.pro_enddate = endDate

            # Validate Price
            price = request.POST['productPrice'].replace(',', '.')
            if not productQueries.validatePrice(price):
                raise ValueError('El precio debe ser numérico y separado por punto')

            price = float(price)
            if price <= 0:
                raise ValueError('El precio debe ser mayor a 0')
            if len(str(price).split('.')[1]) > 2:
                raise ValueError('El precio debe tener máximo 2 decimales')
            newProduct.pro_price = price
            productQueries.saveProduct(newProduct)

            return productsModule(request, userId)
        except ValueError as e:
            errorMessage = str(e)
            return addProductsTemplate(request, template, user, errorMessage)
        except modExceptions.productModuleError as e:
            errorMessage = str(e)
            return addProductsTemplate(request, template, user, errorMessage)
    else:
        try:
            user = userQueries.getUserById(userId)
            return addProductsTemplate(request, template, user)
        except modExceptions.productModuleError as e:
            errorMessage = str(e)
            return productsTemplate(request, template, user, errorMessage)

def productsTemplate(request, template, user, productsList, error=None):    
    return render(request, template, {
            'user': user,
            'productsList': productsList,
            'error': error
            })

def addProductsTemplate(request, template, user, error=None):
    return render(request, template, {
            'user': user,
            'error': error
            })