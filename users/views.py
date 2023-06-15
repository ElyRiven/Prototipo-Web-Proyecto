from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from users.models import User, Role
from users.authentication import utils

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = utils.getUserByEmail(email)
            if user:
                if utils.checkPassword(user, password):
                    if utils.checkRole(user):
                        return redirect('users')
                    else:
                        return render(request, 'login.html', {'error': 'Usuario no autorizado'})
                else:
                    return render(request, 'login.html', {'error': 'Contraseña Incorrecta'})
            else:
                return render(request, 'login.html', {'error': 'Usuario Incorrecto'})
        except utils.UserLoginError:
            return render(request, 'login.html', {'error': 'Error al iniciar sesión'})
    else:
        return render(request, 'login.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usersModule(request):
    return render(request, 'users.html')