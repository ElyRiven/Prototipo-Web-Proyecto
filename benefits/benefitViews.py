from django.urls import reverse
from django.shortcuts import render, redirect
from benefits.utilsModule import queries as benefitQueries
from benefits.utilsModule import modExceptions
from benefits.models import User, Benefit
from datetime import datetime

def benefitModule(request, userId):
    productsList = None
    template = 'benefits.html'
    try:
        user = benefitQueries.getUserById(userId)
        benefitsList = benefitQueries.getBenefits()
        return benefitTemplate(request, template, user, benefitsList=benefitsList)
    except modExceptions.benefitModuleError as e:
        return benefitTemplate(request, template, user, error=str(e))

def addBenefit(request, userId):
    template = 'benefitsAdd.html'
    if request.method == 'POST':
        try:
            user = benefitQueries.getUserById(userId)
            newBenefit = Benefit()
            newBenefit = assignBenefit(newBenefit,
                                        request.POST['benefitName'].upper(),
                                        request.POST['benefitType'].upper(),
                                        request.POST['benefitDescription'].upper())
            benefitQueries.saveBenefit(newBenefit)
            url = reverse('benefits', kwargs={'userId': userId})
            return redirect(url)
        except modExceptions.benefitModuleError as e:
            return benefitTemplate(request, template, user, error=str(e))
    else:
        try:
            user = benefitQueries.getUserById(userId)
            return benefitTemplate(request, template, user)
        except modExceptions.benefitModuleError as e:
            return benefitTemplate(request, template, user, error=str(e))

def editBenefit(request, userId, benefitId):
    template = 'benefitsUpdate.html'
    if request.method == 'POST':
        try:
            user = benefitQueries.getUserById(userId)
            benefit = benefitQueries.getBenefitById(benefitId)
            benefit = assignBenefit(benefit,
                                        request.POST['benefitName'].upper(),
                                        request.POST['benefitType'].upper(),
                                        request.POST['benefitDescription'].upper())
            benefitQueries.saveBenefit(benefit)
            url = reverse('benefits', kwargs={'userId': userId})
            return redirect(url)
        except modExceptions.benefitModuleError as e:
            return benefitTemplate(request, template, user, error=str(e))
    else:
        try:
            user = benefitQueries.getUserById(userId)
            benefit = benefitQueries.getBenefitById(benefitId)
            return benefitTemplate(request, template, user, benefit=benefit)
        except modExceptions.benefitModuleError as e:
            return benefitTemplate(request, template, user, error=str(e))

def deleteBenefit(request, userId, benefitId):
    template = 'benefits.html'
    try:
        user = benefitQueries.getUserById(userId)
        benefit = benefitQueries.getBenefitById(benefitId)
        benefitQueries.deleteBenefit(benefit)
        url = reverse('benefits', kwargs={'userId': userId})
        return redirect(url)
    except modExceptions.benefitModuleError as e:
        return benefitTemplate(request, template, user, error=str(e))

def benefitUserList(request, userId, benefitId):
    template = 'benefitsUserList.html'
    try:
        user = benefitQueries.getUserById(userId)
        benefit = benefitQueries.getBenefitById(benefitId)
        useBenList = benefitQueries.getUserBenefitList(benefitId)
        return benefitTemplate(request, template, user, benefit=benefit, useBenList=useBenList)
    except modExceptions.benefitModuleError as e:
        return benefitTemplate(request, template, user, error=str(e))

def benefitLog(request, userId, benefitId):
    template = 'benefitsLog.html'
    try:
        user = benefitQueries.getUserById(userId)
        benefit = benefitQueries.getBenefitById(benefitId)
        benLogList = benefitQueries.getBenefitLogList(benefitId)
        return benefitTemplate(request, template, user, benefit=benefit, benLogList=benLogList)
    except modExceptions.benefitModuleError as e:
        return benefitTemplate(request, template, user, error=str(e))

def assignBenefit(benefit, benName, benType, benDescription):
    benefit.ben_name = benName
    benefit.ben_type = benType
    benefit.ben_description = benDescription
    return benefit

def benefitTemplate(request, template, user, benefit=None, benefitsList=None, useBenList=None, benLogList=None, countryList=None, questionList=None,error=None):    
    return render(request, template, {
            'user': user,
            'benefit': benefit,
            'benefitsList': benefitsList,
            'useBenList': useBenList,
            'benLogList': benLogList,
            'countryList': countryList,
            'questionList': questionList,
            'error': error
            })