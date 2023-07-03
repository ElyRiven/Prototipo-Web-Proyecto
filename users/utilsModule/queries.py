from users.models import User, Role, Benefit, UserBenefit
from users.utilsModule import modExceptions
from django.db import IntegrityError

#Users List
def getUsers():
    try:
        return User.objects.all().order_by('use_firstname')
    except User.DoesNotExist:
        return None

#Logged User
def getUserById(userId):
    try:
        return User.objects.get(use_code=userId)
    except User.DoesNotExist:
        raise modExceptions.userModuleError('No se encontro el usuario especificado')

#Save/Update New User
def saveUser(user):
    try:
        user.save()
        return True
    except User.CreationError:
        raise modExceptions.userModuleError('Ocurrio un error al guardar el usuario')

#Delete User
def deleteUser(userId):
    try:
        benefitList = Benefit.objects.all()
        for benefit in benefitList:
            userBenefit = UserBenefit.objects.get(use_code=userId, ben_code=benefit.ben_code)
            userBenefit.delete()
        user = User.objects.get(use_code=userId)
        user.delete()
        return True
    except User.DoesNotExist:
        raise modExceptions.userModuleError('Ocurrio un error al eliminar el usuario')

#Add Benefit to User
def addBenefitToUser(user):
    try:
        benefitList = Benefit.objects.all()
        user = User.objects.get(use_code=user.use_code)
        for benefit in benefitList:
            userBenefit = UserBenefit()
            userBenefit.use_code = user
            userBenefit.ben_code = benefit
            userBenefit.save()
        return True
    except User.DoesNotExist:
        raise modExceptions.userModuleError('Ocurrio un error al agregar los beneficios al usuario')

#Get Role by Id
def getRoleById(roleId):
    try:
        return Role.objects.get(rol_code=roleId)
    except Role.DoesNotExist:
        raise modExceptions.userModuleError('No se encontro el rol especificado')

#Roles List
def getRoles():
    try:
        return Role.objects.all().order_by('rol_name')
    except Role.DoesNotExist:
        raise modExceptions.roleModuleError('No se encontraron roles registrados')

#Save New Role
def saveNewRole(newRole):
    try:
        newRole.save()
        return True
    except User.DoesNotExist:
        raise modExceptions.roleModuleError('Ocurrio un error al guardar el rol')

#Update Role
def updateRole(roleId, roleName):
    try:
        role = Role.objects.get(rol_code=roleId)
        role.rol_name = roleName
        role.save()
        return True
    except Role.DoesNotExist:
        raise modExceptions.roleModuleError('Ocurrio un error al actualizar el rol')

#Delete Role
def deleteRole(roleId):
    try:
        role = Role.objects.get(rol_code=roleId)
        role.delete()
        return True
    except IntegrityError:
        raise modExceptions.roleModuleError('No se puede borrar el registro. Existen usuarios asignados a este rol')