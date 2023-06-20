from users.models import User, Role
import hashlib

#Check if user exists
def getUserByEmail(email):
    try:
        return User.objects.get(use_email=email.upper())
    except User.DoesNotExist:
        return None

#Check password with hash pending
def checkPassword(user, password):
    encryptedPassword = encryptPassword(password)
    try:
        return user.use_password == encryptedPassword
    except User.PasswordDoesNotExist:
        return None

#Check if user has admin role
def checkRole(user):
    try:
        adminRole = Role.objects.get(rol_name='ADMIN')        
        return user.rol_code.rol_code == adminRole.rol_code
    except Role.DoesNotExist:
        return None

def encryptPassword(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()