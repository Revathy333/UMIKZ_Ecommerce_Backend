from django.db import models
from django.contrib.auth.models import User

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    image = models.TextField(blank=True, null=True)  
    
    def __str__(self):
        return f"{self.user.username}'s profile"