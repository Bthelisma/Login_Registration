# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def register_validate(self, postData):
        errors = []

        if not postData['first_name'] or not postData['last_name'] or not postData['email'] or not postData['password'] or not postData['cpassword']:
            errors.append( "All fields are required")
                # check name
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors.append( "name fields should be at least 3 characters")
        if not NAME_REGEX.match(postData['first_name']) or not NAME_REGEX.match(postData['last_name']):
            errors.append( "name is not valid")
                # check email
        if len(postData['email'].lower()) < 1:
            errors.append( "Email cannot be blank")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append( "Email is not valid")
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors.append("email is not unique")
                # check password
        if len(postData['password'] )< 8:
            errors.append ( "password must be at least 8 characters")
        elif postData['password'] != postData['cpassword']:
            errors.append ( "password must be match")

        if not errors:
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                first_name=postData['first_name'],
                last_name=postData['last_name'],
                email=postData['email'],
                password=hashed
            )
            return new_user

        return errors

    def login_validate(self, postData):
        errors = []
                # check DB for email
        if len(self.filter(email=postData['email'])) > 0:
                # check user's password
            user = self.filter(email=postData['email'])[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors.append('login failed')
        else:
            errors.append('Invalid login info')

        if errors:
            return errors
        return user

class User(models.Model):
      first_name = models.CharField(max_length=255)
      last_name = models.CharField(max_length=255)
      email = models.CharField(max_length=255)
      password = models.CharField(max_length=255)
      created_at = models.DateTimeField(auto_now_add = True)
      updated_at = models.DateTimeField(auto_now = True)

      objects = UserManager()
