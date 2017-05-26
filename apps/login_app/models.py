# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    # def validate_me(self, first_name, last_name, email, password, confirm_password):
    def validate_me(self, postData):
        error = []
        #get info from postData: purely for readability
        f_n = postData['first_name']
        l_n = postData['last_name']
        eml = postData['email']
        pwd = postData['password']
        c_pwd = postData['confirm_password']

        #validations
        if len(f_n) <= 2 or not f_n.isalpha():
            error.append('First name invalid.')
        if len(l_n) <= 2 or not l_n.isalpha():
            error.append('Last name is not valid.')
        if not EMAIL_REGEX.match(eml):
            error.append('Email is invalid')
        if len(pwd) < 8 or pwd != c_pwd:
            error.append('Passwords do not match.')
        #check that given email is not already stored in user table
        users = User.objects.all()
        for user in users:
            if eml == user.email:
                error.append('Email already registered.')
        #if there are no errors with user inputs:
        if len(error) == 0:
            u = User.objects.create(first_name=f_n, last_name=l_n, email=eml, password=pwd)
            return [True, u]
        #if there are errors with user inputs
        else:
            return [False, error]
    def login(self, postData):
        #get email from postData: just for readability
        eml = postData['email']
        pwd = postData['password']
        #check if there is a match in registered users
        users = User.objects.all()
        for user in users:
            #if there is a match, login
            if eml == user.email and pwd == user.password:
                return [True, user.id]
        #if there is no match, error
        return [False, False]

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return 'id: '+str(self.id)