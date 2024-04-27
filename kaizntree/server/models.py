# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import EmailValidator
from datetime import datetime

class User(models.Model):
    email_address = models.EmailField(validators=[EmailValidator()], unique=True, null=True)
    password = models.CharField(max_length=150)
    created_at = models.DateTimeField(default=datetime.now)

    def set_password(self, original):
        self.password = make_password(original)

    def validate_password(self, original):
        return check_password(original, self.password)

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Item(models.Model):
    sku = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    in_stock = models.DecimalField(max_digits=10, decimal_places=3)
    available_stock = models.DecimalField(max_digits=10, decimal_places=3)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    units = models.CharField(max_length=100, null=True)
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    desired_stock = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)