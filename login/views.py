from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.models import User, Group
#from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from AP.models import AP
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    if request.user.groups.filter(name='professor').count() > 0:
        return HttpResponseRedirect(reverse('aps:index'))
    else:
        if request.user.is_authenticated():
            aps = AP.objects.all().filter(publicado=True)
            return render(request, 'painel.html', {'aps': aps})
        else:
            return render(request, 'login.html')

def registrar(request):
    try:
        if (request.POST['username'] != "" and request.POST['email'] != ""
         and request.POST['password'] != "" and request.POST['first_name'] != "") :
            
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            
            user.save()
            
            return render(request, 'login.html', {
                'sucess_message': "Registrado com sucesso! Efetue seu login agora mesmo!"
            })
        else:
            return render(request, 'login.html', {
                'error_message': "Campos com probelmas de autenticidade, reveja!"
            })
    except IntegrityError:
        return render(request, 'login.html', {
                'error_message': "Username validado, ativo e autenticado, defina outro nickname."
            })

def logar(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    
    if user is not None:
        # the password verified for the user
        if user.is_active:
            login(request, user)
            if user.groups.filter(name='professor').count() > 0:
                response = HttpResponseRedirect(reverse('aps:index'))
            else:
                response = HttpResponseRedirect(reverse('login:login'))
            return response
        else:
            return render(request, 'login.html', {
                'error_message': "Senha validada, mas a conta desabilitada. Contate o Administrador!",
            })
    else:
        # the authentication system was unable to verify the username and password
        return render(request, 'login.html', {
                'error_message': "Nickname e senha incoerentes!",
            })

@login_required
def logout(request):
    # try:
    #    del request.session['perfil_user']
    #   del request.session['perfil_user_tipo']
    #   del request.session['ipuser']
    # except KeyError:
    #   pass
    
    #python is calling the wrong logout method (yours and not django's). 
    #I would instead qualify the logout method you are calling
    auth.logout(request)
    
    return render(request, 'login.html', {'sucess_message': "Desconectado!"})