from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):

    def register_validator(self, postData):
        
        errors = {}
        
        # add keys and values to errors dictionary for each invalid field
        if len(postData['name']) < 3:
            errors["name"] = "Name should be at least 3 characters"

        username_check = self.filter(username=postData['username'])
        if username_check:
            errors['username'] = "Username already in use"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 9 characters"
        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Passwords dont match"

     
        return errors

    def authenticate(self, username, password):
        users = self.filter(username=username)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            name = form['name'],   
            username = form['username'],
            password = pw
            
        )
class User(models.Model):
    name =models.CharField(max_length=100)
    username =models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    objects = UserManager()

class WishlistManager(models.Manager):
    def wishlist_validator(self, postData):
        errors = {}

        if len(postData['item_name']) < 1:
            errors['item_name'] = "Title must not be blank."   

        return errors

class Wishlist(models.Model):
    item_name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="created_items", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    wishlisted_by = models.ManyToManyField(User, related_name="wishlisted_items")
    objects = WishlistManager()