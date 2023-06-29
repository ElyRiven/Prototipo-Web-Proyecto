from django.urls import reverse
from django.shortcuts import render, redirect
from benefits.utilsModule import queries as questionaryQueries
from benefits.utilsModule import modExceptions
from benefits.models import User, Country, Question
from datetime import datetime

def questionaryModule(request, userId):
    template = 'questionaries.html'
    try:
        user = questionaryQueries.getUserById(userId)
        countryList = questionaryQueries.getCountryList()
        return questionaryTemplate(request, template, user, countryList=countryList)
    except modExceptions.questionaryModuleError as e:
        return questionaryTemplate(request, template, user, error=str(e))

def addCountry(request, userId):
    template='questionariesAdd.html'
    if request.method == 'POST':
        try:
            user = questionaryQueries.getUserById(userId)
            newCountry = Country()
            newCountry.cou_name = request.POST['countryName'].upper()
            questionaryQueries.saveCountry(newCountry)
            url = reverse('questionaries', kwargs={'userId': userId})
            return redirect(url)
        except modExceptions.questionaryModuleError as e:
            return questionaryTemplate(request, template, user, error=str(e))
    else:
        try:
            user = questionaryQueries.getUserById(userId)
            return questionaryTemplate(request, template, user)
        except modExceptions.questionaryModuleError as e:
            return questionaryTemplate(request, template, user, error=str(e))

def deleteCountry(request, userId, countryId):
    template = 'questionaries.html'
    try:
        user = questionaryQueries.getUserById(userId)
        countryList = questionaryQueries.getCountryList()
        country = questionaryQueries.getCountryById(countryId)
        questionaryQueries.deleteCountry(country)
        url = reverse('questionaries', kwargs={'userId': userId})
        return redirect(url)
    except modExceptions.questionaryModuleError as e:
        return questionaryTemplate(request, template, user, countryList=countryList, error=str(e))

def questionModule(request, userId, countryId):
    template = 'questions.html'
    try:
        user = questionaryQueries.getUserById(userId)
        selectedCountry = questionaryQueries.getCountryById(countryId)
        questionList = questionaryQueries.getQuestionList(countryId)
        return questionaryTemplate(request, template, user, selectedCountry=selectedCountry, questionList=questionList)
    except modExceptions.questionaryModuleError as e:
        return questionaryTemplate(request, template, user, error=str(e))

def addQuestion(request, userId, countryId):
    template = 'questionsAdd.html'
    if request.method == 'POST':
        try:
            user = questionaryQueries.getUserById(userId)
            selectedCountry = questionaryQueries.getCountryById(countryId)
            newQuestion = Question()
            newQuestion = assignQuestion(newQuestion,
                                         request.POST['questionDescription'].upper(),
                                         request.POST['questionAnswer'].upper(),
                                         selectedCountry)
            questionaryQueries.saveQuestion(newQuestion)
            url = reverse('questions', kwargs={'userId': userId, 'countryId': countryId})
            return redirect(url)
        except modExceptions.questionaryModuleError as e:
            return questionaryTemplate(request, template, user, error=str(e))
    else:
        try:
            user = questionaryQueries.getUserById(userId)
            return questionaryTemplate(request, template, user)
        except modExceptions.questionaryModuleError as e:
            return questionaryTemplate(request, template, user, error=str(e))

def editQuestion(request, userId, countryId, questionId):
    template = 'questionsUpdate.html'
    if request.method == 'POST':
        try:
            user = questionaryQueries.getUserById(userId)
            selectedCountry = questionaryQueries.getCountryById(countryId)
            question = questionaryQueries.getQuestionById(questionId)
            question = assignQuestion(question,
                                        request.POST['questionDescription'].upper(),
                                        request.POST['questionAnswer'].upper(),
                                        selectedCountry)
            questionaryQueries.saveQuestion(question)
            url = reverse('questions', kwargs={'userId': userId, 'countryId': countryId})
            return redirect(url)
        except modExceptions.questionaryModuleError as e:
            return questionaryTemplate(request, template, user, error=str(e))
    else:
        try:
            user = questionaryQueries.getUserById(userId)
            selectedQuestion = questionaryQueries.getQuestionById(questionId)
            return questionaryTemplate(request, template, user, selectedQuestion=selectedQuestion)
        except modExceptions.questionaryModuleError as e:
            return questionaryTemplate(request, template, user, error=str(e))

def deleteQuestion(request, userId, countryId, questionId):
    template = 'questions.html'
    try:
        user = questionaryQueries.getUserById(userId)
        question = questionaryQueries.getQuestionById(questionId)
        questionaryQueries.deleteQuestion(question)
        url = reverse('questions', kwargs={'userId': userId, 'countryId': countryId})
        return redirect(url)
    except modExceptions.questionaryModuleError as e:
        return questionaryTemplate(request, template, user, error=str(e))

def assignQuestion(question, description, answer, country):
    question.que_description = description
    question.que_answer = answer
    question.cou_code = country
    return question

def questionaryTemplate(request, template, user, countryList=None, selectedCountry=None, questionList=None, selectedQuestion=None, error=None):    
    return render(request, template, {
            'user': user,
            'countryList': countryList,
            'selectedCountry': selectedCountry,
            'questionList': questionList,
            'selectedQuestion': selectedQuestion,
            'error': error
            })