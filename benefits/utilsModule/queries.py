from benefits.models import User, Benefit, UserBenefit, BenefitLog, Country, Question
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
        raise modExceptions.questionaryModuleError('No se encontró el registro solicitado')

# Get all Benefits
def getBenefits():
    try:
        return Benefit.objects.all().order_by('ben_type')
    except Benefit.DoesNotExist:
        raise modExceptions.questionaryModuleError('No se encontraron beneficios registrados')

# Save/Update Benefit
def saveBenefit(benefit):
    try:
        benefit.save()
        return True
    except IntegrityError:
        raise modExceptions.questionaryModuleError('Error al guardar el beneficio')
    
# Delete Benefit
def deleteBenefit(benefit):
    try:
        benefit.delete()
        return True
    except IntegrityError:
        raise modExceptions.questionaryModuleError('Error al eliminar el beneficio')

# Get all UserBenefit registers
def getUserBenefitList(benefitId):
    try:
        return UserBenefit.objects.filter(ben_code=benefitId).order_by('useben_state')
    except UserBenefit.DoesNotExist:
        raise modExceptions.questionaryModuleError('No se encontraron registros en la base de datos')

# Get all BenefitLog registers
def getBenefitLogList(benefitId):
    try:
        return BenefitLog.objects.filter(ben_code=benefitId).order_by('benlog_date')
    except BenefitLog.DoesNotExist:
        raise modExceptions.questionaryModuleError('No se encontraron registros en la base de datos')

# Get Country List
def getCountryList():
    try:
        return Country.objects.all().order_by('cou_name')
    except Country.DoesNotExist:
        raise modExceptions.questionaryModuleError('No se encontraron registros en la base de datos')

# Get Country by Id
def getCountryById(countryId):
    try:
        return Country.objects.get(cou_code=countryId)
    except Country.DoesNotExist:
        raise modExceptions.questionaryModuleError('No se encontró el registro solicitado')

# Save Country
def saveCountry(country):
    try:
        country.save()
        return True
    except IntegrityError:
        raise modExceptions.questionaryModuleError('Error al guardar el país')

# Delete Country
def deleteCountry(country):
    try:
        country.delete()
        return True
    except IntegrityError:
        raise modExceptions.questionaryModuleError('No se puede elimiar el Pais, existen registros de preguntas asociados')

# Get Questions List by Country
def getQuestionList(countryId):
    try:
        return Question.objects.filter(cou_code=countryId).order_by('que_description')
    except Question.DoesNotExist:
        raise modExceptions.questionaryModuleError('No se encontraron registros en la base de datos')

# Get Question by Id
def getQuestionById(questionId):
    try:
        return Question.objects.get(que_code=questionId)
    except Question.DoesNotExist:
        raise modExceptions.questionaryModuleError('No se encontró el registro solicitado')

# Save/Update Question
def saveQuestion(question):
    try:
        question.save()
        return True
    except IntegrityError:
        raise modExceptions.questionaryModuleError('Error al guardar la pregunta')

# Delete Question
def deleteQuestion(question):
    try:
        question.delete()
        return True
    except IntegrityError:
        raise modExceptions.questionaryModuleError('Error al eliminar la pregunta')