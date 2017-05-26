# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.

#main login/register landing page
def index(request):
    return render(request, 'login_app/index.html')

#route when user submits registration form
def register_process(request):
    if request.method == "POST":
        #get registration form user inputs
        postData = {
            'first_name' : request.POST['first_name'],
            'last_name' : request.POST['last_name'],
            'email' : request.POST['email'],
            'password' : request.POST['password'],
            'confirm_password' : request.POST['confirm_password']
        }

        #validate inputs. if valid, create user
        user = User.objects.validate_me(postData)

        #if user was valid & created
        if user[0] == True:
            request.session['login'] = user[1].id
            return redirect('/success')
        #if user was invalid & not created
        else:
            errors = user[1]
            for error in errors:
                messages.add_message(request, messages.INFO, error)
            return redirect('/')

#login process
def login(request):
    if request.method == "POST":
        #get login form user inputs
        postData = {
            'email' : request.POST['email'],
            'password' : request.POST['password']
        }
        #check for matches in stored users
        #if there is a match, login
        user = User.objects.login(postData)
        #if logged in, set session
        if user[0] == True:
            request.session['login'] = user[1]
            return redirect('/success')
        #if not logged in, add error message
        else:
            messages.add_message(request, messages.INFO, 'Invalid login')
            return redirect('/')

#route to success page on successful login/registration
def success(request):
    context = {
        'user' : User.objects.get(pk=request.session['login'])
    }
    return render(request, 'login_app/success.html', context)


# # # # # # #
# DEBUGGING #
# # # # # # #

#show users - debugging page
def show(request):
    context = {
        'users' : User.objects.all()
    }
    return render(request, 'login_app/show.html', context)

#delete user - debugging page
def delete(request, id):
    user = User.objects.get(pk=id)
    user.delete()
    return redirect('/show')