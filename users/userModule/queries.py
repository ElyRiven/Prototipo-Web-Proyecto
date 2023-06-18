from users.models import User

#Usuario Loggeado
def getUserById(userId):
    try:
        return User.objects.get(use_code=userId)
    except User.DoesNotExist:
        return None
    
def getUsers():
    try:
        return User.objects.all()
    except User.DoesNotExist:
        return None