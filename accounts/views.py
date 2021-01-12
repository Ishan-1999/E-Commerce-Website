from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                Umsg = 'Username Taken.'
                params = {"Umsg": Umsg}
                return render(request, 'register.html', params)
            elif User.objects.filter(email=email).exists():
                Emsg = 'Email already registered.'
                params = {"Emsg": Emsg}
                return render(request, 'register.html', params)
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                return redirect('login')
        else:
            Pmsg = 'Password not matching.'
            params = {"Pmsg": Pmsg}
            return render(request, 'register.html', params)
        
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            msg = 'Your username or password is incorrect.'
            params = {'msg' :msg}
            return render(request, 'login.html', params)
    else:    
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')