from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Create your models here.
class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    default_phone_number= models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    default_town_or_city = models.CharField(
        max_length=40,
        null=True,
        blank=True
        )
    default_street_address1 = models.CharField(
        max_length=80,
        blank=True,
        null=True
    )
    default_street_address2 = models.CharField(
        max_length=80,
        blank=True,
        null=True
    )
    default_county = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    default_postcode = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    default_country = CountryField(
        blank_label='Country *',
        null=True,
        blank=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )
    updated_on = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"