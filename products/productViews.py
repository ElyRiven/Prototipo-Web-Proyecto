from django.shortcuts import render
from users.utilsModule import queries as userQueries
from products.utilsModule import queries as productQueries
from products.utilsModule import modExceptions
from products.models import User, Product, Place

def productsModule(request, userId):
    try:
        user = userQueries.getUserById(userId)
        productsList = productQueries.getProducts()
        return render(request, 'products.html', {
            'user': user,
            'productsList': productsList,
            'module': 'Productos',
            'title': 'Listado de Productos',
            'buttonAddProduct': 'Agregar Producto'
            })
    except modExceptions.productModuleError:
        return render(request, 'products.html', {
            'user': user,
            'error': 'Error al cargar el módulo de productos',
            'module': 'Productos',
            'title': 'Listado de Productos',
            'buttonAddProduct': 'Agregar Producto'
            })