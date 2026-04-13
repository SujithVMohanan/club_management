from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")

        user = self.model(
            username=username,
            **extra_fields
        )

        user.set_password(password)  # hashes password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, password, **extra_fields)
    



class Users(AbstractBaseUser, PermissionsMixin, BaseModel):

    username = models.CharField(
        _('username'),
        max_length=100,
        unique=True
    )

    name = models.CharField(max_length=100, blank=True, null=True)

    home_name = models.CharField(
        _('home name'),
        max_length=250,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()   # ✅ connect manager

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    class Meta:
        ordering = ['id']
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.username}"