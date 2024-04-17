from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return f"{self.full_name} ({self.email})"
    
    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
       return self.is_admin

    def has_perm(self, perm, obj=None):
       return self.is_admin

    def has_module_perms(self, app_label):
       return self.is_admin

    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value
    
    class Meta:
        db_table = "auth_user"



class VerificationToken(models.Model):
    token = models.CharField(max_length=40, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=True);


    def __str__(self):
        return f"{self.user.full_name} ({self.token})"