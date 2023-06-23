from products.models import User, Product, Place
from products.utilsModule import modExceptions
from django.db import IntegrityError

# Get all Products
def getProducts():
    try:
        return Product.objects.all().order_by('pro_name')
    except Product.DoesNotExist:
        raise modExceptions.productModuleError('No se encontraron productos registrados')

# Save a new Product
def saveProduct(newProduct):
    try:
        newProduct.save()
        return True
    except IntegrityError:
        raise modExceptions.productModuleError('Error al registrar el producto')
    
# Validate Price
def validatePrice(price):
    try:
        float(price)
        return True
    except ValueError:
        return False