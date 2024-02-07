from django.db import models
import bcrypt
import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name should be at least 2 characters.'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last Name should be at least 2 characters.'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address.'
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email'] = 'Email already in use.'
        if len(postData['password']) < 8:
            errors['last_name'] = 'Password should be at least 8 characters.'
        if postData['password'] != postData['confirm']:
            errors['confirm'] = 'Passwords do not match.'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(id=id)