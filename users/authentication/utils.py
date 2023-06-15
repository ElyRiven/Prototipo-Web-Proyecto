from users.models import User, Role

#Authentication functions
def getUserByEmail(email):
    try:
        return User.objects.get(use_email=email.upper())
    except User.DoesNotExist:
        return None

#Check password with hash pending
def checkPassword(user, password):
    try:
        print(user.use_password)
        return user.use_password == password
    except User.PasswordDoesNotExist:
        return None

def checkRole(user):
    try:
        adminRole = Role.objects.get(rol_name='ADMIN')        
        return user.rol_code.rol_code == adminRole.rol_code
    except Role.DoesNotExist:
        return None

#Authentication Exceptions
class UserLoginError(Exception):
    pass