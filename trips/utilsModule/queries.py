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

# Get all Users
def getUsers():
    try:
        return User.objects.all().order_by('use_firstname')
    except User.DoesNotExist:
        raise modExceptions.tripModuleError('No se encontraron usuarios registrados')

# Get Product by Id
def getProductById(productId):
    try:
        return Product.objects.get(pro_code=productId)
    except Product.DoesNotExist:
        raise modExceptions.tripModuleError('No se encontraron productos registrados')

# Get all User Products by Product Id
def userProductList(productId):
    try:
        return UserProduct.objects.filter(pro_code=productId).order_by('usepro_state')
    except UserProduct.DoesNotExist:
        raise modExceptions.tripModuleError('Ocurrion un error al obtener los registros')

# Get User Product record by User Id and Product Id
def getUserProduct(userId, productId):
    try:
        return UserProduct.objects.get(use_code=userId, pro_code=productId)
    except UserProduct.DoesNotExist:
        return None
    except UserProduct.MultipleObjectsReturned:
        raise modExceptions.tripModuleError('El usuario tiene varios registros para el mismo producto')

# Create UserProduct record
def saveUserProduct(record):
    try:
        record.save()
    except IntegrityError:
        raise modExceptions.tripModuleError('El usuario ya tiene asignado el producto')

# Get all Appointments by User Id
def getAppointments(user, product):
    try:
        return Appointment.objects.filter(use_code=user, pro_code=product)
    except Appointment.DoesNotExist:
        raise modExceptions.tripModuleError('No se encontraron citas registradas')

# Set UserProduct record to 'IN PROGRESS'
def activateTrip(productId):
    try:
        confirmedList = UserProduct.objects.filter(pro_code=productId, usepro_state='CONFIRMED')
        canceledList = UserProduct.objects.filter(pro_code=productId, usepro_state='PENDING')
        for record in confirmedList:
            record.usepro_state = 'IN PROGRESS'
            record.save()
        for record in canceledList:
            record.usepro_state = 'CANCELED'
            record.save()
    except UserProduct.DoesNotExist:
        raise modExceptions.tripModuleError('No se encontraron registros para activar')