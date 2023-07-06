from api.models import User, Role
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