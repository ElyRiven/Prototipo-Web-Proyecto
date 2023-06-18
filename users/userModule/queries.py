from users.models import User, Role

#Logged User
def getUserById(userId):
    try:
        return User.objects.get(use_code=userId)
    except User.DoesNotExist:
        return None

#Users List
def getUsers():
    try:
        return User.objects.all()
    except User.DoesNotExist:
        return None

#Get Role by Id
def getRoleById(roleId):
    try:
        return Role.objects.get(rol_code=roleId)
    except Role.DoesNotExist:
        return None

#Roles List
def getRoles():
    try:
        return Role.objects.all()
    except Role.DoesNotExist:
        return None
    
#Save New Role
def saveNewRole(roleName):
    try:
        role = Role(rol_name=roleName)
        role.save()
        return True
    except Role.CreationError:
        return None

#Update Role
def updateRole(roleId, roleName):
    try:
        role = Role.objects.get(rol_code=roleId)
        role.rol_name = roleName
        role.save()
        return True
    except Role.DoesNotExist:
        return None
    
#Delete Role
def deleteRole(roleId):
    try:
        role = Role.objects.get(rol_code=roleId)
        role.delete()
        return True
    except Role.DoesNotExist:
        return None