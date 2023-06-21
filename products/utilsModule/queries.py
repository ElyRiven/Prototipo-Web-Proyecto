from products.models import User, Product, Place

# Get all Products
def getProducts():
    try:
        return Product.objects.all().order_by('pro_name')
    except Product.DoesNotExist:
        return None