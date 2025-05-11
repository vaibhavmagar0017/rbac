from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICE = (
        ('admin', 'Admin'),
        ('employee', 'Employee')
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICE, default='employee')



class Record(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    role = models.CharField(max_length=10, choices=CustomUser.ROLE_CHOICE, default='employee')

    def __str__(self):
        return f"{self.user} {self.title} {self.description}"