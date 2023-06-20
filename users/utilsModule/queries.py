from users.models import User, Role, Benefit, UserBenefit

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
        return None

#Save New User
def saveUser(user):
    try:
        user.save()
        return True
    except User.CreationError:
        return None

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
        return None

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
        return Role.objects.all().order_by('rol_name')
    except Role.DoesNotExist:
        return None

#Save New Role
def saveNewRole(newRole):
    try:
        newRole.save()
        return True
    except User.DoesNotExist:
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