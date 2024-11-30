import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser

from rest_framework_simplejwt.tokens import AccessToken, TokenError

GENDER = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

def validate_phone_number(value):
    phone_number_pattern = re.compile(r'^\d{4,15}$')
    if not phone_number_pattern.match(value):
        raise ValidationError('Invalid phone number format.')

class Philatelist(AbstractBaseUser, models.Model):
    profile_img = models.ImageField(upload_to="profiles/", null=True, blank=True)
    
    name = models.CharField(max_length=120, blank=True)
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=15,  # Adjust length as needed
        unique=True,
        validators=[validate_phone_number],
        null=True, blank=True
    )
    
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True)
    address = models.TextField(null=True, blank=True) 
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
    
    is_active = models.BooleanField(
        default=False,
        help_text="Designates whether this user should be treated as active."
    )
    
    access_token = models.TextField(null=True, blank=True)
    valid_otp = models.PositiveIntegerField(null=True, blank=True)
    # fcm_token = models.TextField(null=True, blank=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']
    
    def __str__(self) -> str:
        return self.name
    
    def generateToken(self):
        """
        return: token, need_for_updation
        """
        try:
            token = AccessToken(self.access_token)

            if self.access_token is not None:
                return str(self.access_token), False
        except TokenError as e:
            pass

        new_token = AccessToken.for_user(self)
        return str(new_token), True
