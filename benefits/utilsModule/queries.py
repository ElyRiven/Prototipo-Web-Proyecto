from benefits.models import User, Benefit, UserBenefit, BenefitLog
from benefits.utilsModule import modExceptions
from django.db import IntegrityError

#Logged User
def getUserById(userId):
    try:
        return User.objects.get(use_code=userId)
    except User.DoesNotExist:
        return None

# Get Benefit by Id
def getBenefitById(benefitId):
    try:
        return Benefit.objects.get(ben_code=benefitId)
    except Benefit.DoesNotExist:
        raise modExceptions.benefitModuleError('No se encontró el registro solicitado')

# Get all Benefits
def getBenefits():
    try:
        return Benefit.objects.all().order_by('ben_type')
    except Benefit.DoesNotExist:
        raise modExceptions.benefitModuleError('No se encontraron beneficios registrados')

# Save/Update Benefit
def saveBenefit(benefit):
    try:
        benefit.save()
        return True
    except IntegrityError:
        raise modExceptions.benefitModuleError('Error al guardar el beneficio')
    
# Delete Benefit
def deleteBenefit(benefit):
    try:
        benefit.delete()
        return True
    except IntegrityError:
        raise modExceptions.benefitModuleError('Error al eliminar el beneficio')

# Get all UserBenefit registers
def getUserBenefitList(benefitId):
    try:
        return UserBenefit.objects.filter(ben_code=benefitId).order_by('useben_state')
    except UserBenefit.DoesNotExist:
        raise modExceptions.benefitModuleError('No se encontraron registros en la base de datos')

# Get all BenefitLog registers
def getBenefitLogList(benefitId):
    try:
        return BenefitLog.objects.filter(ben_code=benefitId).order_by('benlog_date')
    except BenefitLog.DoesNotExist:
        raise modExceptions.benefitModuleError('No se encontraron registros en la base de datos')