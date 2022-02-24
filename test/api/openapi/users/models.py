from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models

from users.validators import USStateValidator


class Address(models.Model):
    number = models.IntegerField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, validators=[USStateValidator()])
    zip = models.CharField(max_length=5,
                           validators=[RegexValidator(regex='^\d{5}$', message='Length of zip code must be 5')])


class User(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    phone = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
