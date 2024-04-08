from django.db import models
from cryptography.fernet import Fernet # handling password encryption
from dotenv import load_dotenv, set_key
from mealGen.env_generator import generate_key_and_update_env

import os 


# Create your models here.

class UserProfile(models.Model):
    """Holds the user's account information"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    dietary_preferences = models.CharField(max_length=100)

class UserAPICredentials(models.Model):
    """Holds the users MyFitnessPal Email and Token"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    _encrypted_password = models.CharField(max_length=255)

    # getter and setter for encrypted password data 
    @property
    def password(self):
        # Retrieve the encryption key from the environment variable
        encryption_key = os.getenv("ENCRYPTION_KEY")
        f = Fernet(encryption_key.encode())

        # Decrypt the password
        return f.decrypt(self._encrypted_password.encode()).decode()

    @password.setter
    def password(self, raw_password):
        # Retrieve the encryption key from the environment variable
        encryption_key = os.getenv("ENCRYPTION_KEY")
        f = Fernet(encryption_key.encode())

        # Encrypt and store the password
        self._encrypted_password = f.encrypt(raw_password.encode()).decode()