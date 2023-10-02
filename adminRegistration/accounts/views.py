from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import cache_control


# from django.http import HttpResponse

# Create your views here.

@cache_control(no_cache=True, no_store=True, must_validate=True)
def home(request):
    return render(request, 'home.html')


@cache_control(no_cache=True, no_store=True, must_validate=True)
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password1']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return render(request, 'home.html', {'name': username})
            else:
                messages.error(request, 'bad credentials')
                return redirect('signin')
        return render(request, 'signin.html')


@cache_control(no_cache=True, no_store=True, must_validate=True)
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    # print('user ...')
    if request.method == 'POST':
        print('post ....')
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request, "username already exists !,Try another username")
            return redirect("signup")
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered.")
            return redirect('signup')
        if password1 != password2:
            messages.error(request, "Password didnt match")
            return redirect('signup')

        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name

        user.save()
        print('user created')
        return render(request, 'signin.html')
    else:
        return render(request, 'base.html')


@cache_control(no_cache=True, no_store=True, must_validate=True)
def signout(request):
    if request.user.is_authenticated:
        logout(request)
    messages.success(request, 'logged out succesfully')
    return redirect('signin')

@cache_control(no_cache=True, no_store=True, must_validate=True)
def admin_panel(request):
    if request.user.is_superuser:

        if request.GET.get('search') is not None:
            search = request.GET.get('search')
            users = User.objects.filter(username__contains=search)
        else:
            users = User.objects.all()
        context = {
            'users': users
        }
        return render(request, 'admin_panel.html', context)
    else:
        return redirect('home')

@cache_control(no_cache=True, no_store=True, must_validate=True)
def delete_user(request, user_id):
    if request.user.is_superuser:

        user = User.objects.get(id=user_id)

        user.delete()

        return redirect('admin_panel')
    else:
        return redirect('home')

@cache_control(no_cache=True, no_store=True, must_validate=True)
def create_user(request):
    if request.user.is_superuser:

        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password1']

            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = first_name
            myuser.last_name = last_name

            myuser.save()
            messages.success(request, 'Account successfully created')
            return redirect('admin_panel')

        return render(request, 'create_user.html')
    else:
        return redirect('home')

@cache_control(no_cache=True, no_store=True, must_validate=True)
def update_user(request, user_id):
    if request.user.is_superuser:

        user = User.objects.get(id=user_id)

        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password = request.POST['password1']

            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.set_password = password

            user.save()
            messages.success(request, 'Updated succesfully')

            return redirect('admin_panel')

        return render(request, 'edit.html', {'user': user})
    else:
        return redirect('home')
