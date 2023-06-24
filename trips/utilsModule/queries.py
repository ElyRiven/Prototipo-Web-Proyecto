from trips.models import User, Product, UserProduct, Appointment
from trips.utilsModule import modExceptions
from django.db import IntegrityError

#Logged User
def getUserById(userId):
    try:
        return User.objects.get(use_code=userId)
    except User.DoesNotExist:
        return None

# Get all Products
def getProducts():
    try:
        return Product.objects.all().order_by('pro_name')
    except Product.DoesNotExist:
        raise modExceptions.tripModuleError('No se encontraron productos registrados')

# Get all User Products by Product Id
def userProductList(productId):
    try:
        return UserProduct.objects.filter(pro_code=productId).order_by('use_code')
    except UserProduct.DoesNotExist:
        raise modExceptions.tripModuleError('Ocurrion un error al obtener los registros')

