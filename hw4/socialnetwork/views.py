from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

from socialnetwork.forms import LoginForm, RegisterForm


# Create your views here.
def login_action(request):
    context = {}
    if request.method == 'GET':
        form = LoginForm()
        context['form'] = form
        return render(request, 'socialnetwork/login.html', context)
    form = LoginForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))


def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


def register_action(request):
    context = {}
    if request.method == 'GET':
        form = RegisterForm()
        context['form'] = form
        return render(request, 'socialnetwork/register.html', context)
    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))



@login_required
def global_stream_action(request):
    context = {}
    name = request.user.first_name + " " + request.user.last_name
    context['name'] = name
    if request.method == 'GET':
        return render(request, 'socialnetwork/global_stream.html', context)


def follower_stream_action(request):
    context = {}
    name = request.user.first_name + " " + request.user.last_name
    context['name'] = name
    if request.method == 'GET':
        return render(request, 'socialnetwork/follower_stream.html', context)


def my_profile_action(request):
    context = {}
    name = request.user.first_name + " " + request.user.last_name
    context['name'] = name
    if request.method == 'GET':
        context['bio'] = "Jeff is a computer scientist. In the summer time he cultivates fig trees."
        return render(request, 'socialnetwork/my_profile.html', context)
    bio = request.POST['bio']
    context['bio'] = bio
    return render(request, 'socialnetwork/my_profile.html', context)



def personal_profile_action(request):
    context = {}
    name = request.user.first_name + " " + request.user.last_name
    context['name'] = name
    if request.method == 'GET':
        username = "Farnam Jahanian"
        context['username'] = username
        context['bio'] = "Farnam is the president of a top-tier university. In the summertime he plays golf."
        return render(request, 'socialnetwork/personal_profile.html', context)
