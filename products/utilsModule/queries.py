from products.models import User, Product, Place
from products.utilsModule import modExceptions
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
        raise modExceptions.productModuleError('No se encontraron productos registrados')

# Get Product by Id
def getProductById(productId):
    try:
        return Product.objects.get(pro_code=productId)
    except Product.DoesNotExist:
        raise modExceptions.productModuleError('No se encontró el producto')

# Save/Update a Product
def saveProduct(newProduct):
    try:
        newProduct.save()
        return True
    except IntegrityError:
        raise modExceptions.productModuleError('Error al registrar el producto')

# Delete a Product
def deleteProduct(productId):
    try:
        product = Product.objects.get(pro_code=productId)
        product.delete()
        return True
    except Product.DoesNotExist:
        raise modExceptions.productModuleError('No se encontró el producto')
    except IntegrityError:
        raise modExceptions.productModuleError('No se puede eliminar el producto, existen registros de lugares asociados')

# Get Places by Product Id
def getPlaceByProductId(productId):
    try:
        return Place.objects.filter(pro_code=productId).order_by('pla_startdate')
    except Place.DoesNotExist:
        raise modExceptions.placeModuleError('No se encontraron lugares registrados')

# Get Place by Id
def getPlaceById(placeId):
    try:
        return Place.objects.get(pla_code=placeId)
    except Place.DoesNotExist:
        raise modExceptions.placeModuleError('No se encontró el lugar')

# Save/Update a Place
def savePlace(newPlace):
    try:
        newPlace.save()
        return True
    except IntegrityError:
        raise modExceptions.placeModuleError('Error al registrar el lugar')