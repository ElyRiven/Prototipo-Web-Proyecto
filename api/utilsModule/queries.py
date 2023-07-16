from api.models import User, Role, Benefit, UserProduct, Product, Country, Question, UserBenefit, BenefitLog
from api.utilsModule import modExceptions
import hashlib

# Encrypt password
def encryptPassword(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()

# Get user by email and password
def validateUser(username, password):
    try:
        user = User.objects.get(use_email=username)
        hashPassword = encryptPassword(password)
        if user.use_password == hashPassword:
            return user
        else:
            return None
    except User.DoesNotExist:
        raise modExceptions.apiException('Usuario no existe')

# Get all Users
def getAllUsers():
    try:
        return User.objects.all()
    except User.DoesNotExist:
        raise modExceptions.apiException('No existen usuarios')

# Get user by email
def getUserById(userId):
    try:
        return User.objects.get(use_code=userId)
    except User.DoesNotExist:
        raise modExceptions.apiException('Usuario no existe')

# Save user
def saveUser(user):
    try:
        user.save()
        return True
    except:
        raise modExceptions.apiException('Error al guardar usuario')

# Get Role by Id
def getRoleById(roleId):
    try:
        return Role.objects.get(rol_code=roleId)
    except Role.DoesNotExist:
        raise modExceptions.apiException('Rol no existe')

# Get all Benefits
def getAllBenefits():
    try:
        return Benefit.objects.all()
    except Benefit.DoesNotExist:
        raise modExceptions.apiException('No existen beneficios')

# Get UserProduct by UserId
def getUserProductByUserId(userId):
    try:
        userProduct = UserProduct.objects.get(use_code=userId, usepro_state='IN PROGRESS')
        return userProduct
    except UserProduct.DoesNotExist:
        raise modExceptions.apiException('El usuario no tiene viajes en progreso')

# Get Product by Id
def getProductById(productId):
    try:
        return Product.objects.get(pro_code=productId)
    except Product.DoesNotExist:
        raise modExceptions.apiException('Producto no existe')

# Get Country by Name
def getCountryByName(countryName):
    try:
        return Country.objects.get(cou_name=countryName)
    except Country.DoesNotExist:
        raise modExceptions.apiException('Pais no existe')

# Get All Question by CountryId
def getAllQuestionByCountryId(countryId):
    try:
        return Question.objects.filter(cou_code=countryId)
    except Question.DoesNotExist:
        raise modExceptions.apiException('No existen preguntas para el pais seleccionado')

# Get all UserBenefit by UserId
def getAllUserBenefitByUserId(userId):
    try:
        return UserBenefit.objects.filter(use_code=userId).order_by('ben_code')
    except UserBenefit.DoesNotExist:
        raise modExceptions.apiException('No existen beneficios para el usuario')

# Get UserBenefit by UserId & BenefitId
def getUserBenefit(userId, benefitId):
    try:
        return UserBenefit.objects.get(use_code=userId, ben_code=benefitId)
    except UserBenefit.DoesNotExist:
        raise modExceptions.apiException('No existen beneficios para el usuario')

# Save UserBenefit by UserId & BenefitId
def saveUserBenefit(updatedUserBenefit):
    try:
        updatedUserBenefit.save()
        return True;
    except UserBenefit.DoesNotExist:
        raise modExceptions.apiException('No se pudo actualizar el estado del beneficio')

# Get Benefit by Id
def getBenefitById(benefitId):
    try:
        return Benefit.objects.get(ben_code=benefitId)
    except Benefit.DoesNotExist:
        raise modExceptions.apiException('Beneficio no existe')

# Save BenefitLog by UserId & BenefitId
def saveBenefitLog(benefitLog):
    try:
        benefitLog.save()
        return True;
    except:
        raise modExceptions.apiException('No se pudo guardar el log del beneficio')