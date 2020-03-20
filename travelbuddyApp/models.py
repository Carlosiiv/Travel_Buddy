from __future__ import unicode_literals
import re
from datetime import date, datetime
from django.db import models

class UserManager(models.Manager):
    def user_validator(self,postData):
        errors = {}
        # username verification/authenticator
        if len(postData['username']) < 2:
            errors['username'] = 'Username must be longer than 2 characters!'
        userName = User.objects.all()
        for un in userName:
            if un.username == postData['username']:
                errors['username'] = 'Username already exist! If this this is not a mistake please login'

        if len(postData['name']) < 2:
            errors['name'] = 'Name must be longer than 2 characters!'
        
        # password validations
        password_REGEX = re.compile(r'[A-Za-z0-9!@#$%^&+=]+[A-Za-z]|[0-9]|[!@#$%^&+=]+[A-Za-z0-9!@#$%^&+=]+$')
        if not password_REGEX.match(postData['password']):
            errors['password'] = "Password must contain atleast 1 Letter, 1 Number, and 1 Symbol"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be atleast 8 characters!"
        if postData['password'] != postData['confirm_password']:
            errors['password'] = 'Passwords must match!'
        return errors

class TripManager(models.Manager):
    def trip_validator(self,postData):
        errors = {}
        
        if len(postData['destination']) < 2:
            errors['destination'] = 'Destination must be filled in!'
        if len(postData['description']) < 2:
            errors['description'] = 'Description must be filled in!'

        # startdate trip_validator
        if postData['startdate'] == '':
           errors['startdate'] = 'Please enter a Start Date!'
        else:
            datetime_object = datetime.strptime(postData['startdate'], '%Y-%m-%d')
            if datetime_object < datetime.today():
                errors['startdate'] = "Start Date must be in the future!"

        # enddate trip_validator
        if postData['enddate'] == '':
           errors['enddate'] = 'Please enter an End Date!'
        else:
            datetime_object = datetime.strptime(postData['startdate'], '%Y-%m-%d')
            datetime_object2 = datetime.strptime(postData['enddate'], '%Y-%m-%d')
            if datetime_object2 < datetime_object:
                errors['enddate'] = "End Date must be in the future in correalation to Start Date!"
        return errors


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    creator = models.ForeignKey(User, related_name="creator", on_delete = models.CASCADE)
    user = models.ManyToManyField(User,related_name="trips")
    destination = models.CharField(max_length=255)
    description = models.TextField()
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()