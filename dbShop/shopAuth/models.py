from django.db import models

# Create your models here.


from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .managers import CustomUserManager
from .token_generators import generate_jwt


# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Адрес электронной почты', unique=True)
    is_staff = models.BooleanField(default=False)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    refresh_token = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self) -> models.EmailField:
        return self.email

    @property
    def access_token(self) -> str:
        return generate_jwt(self.pk)


class Job(models.Model):
    title = models.CharField(max_length=128)
    salary = models.IntegerField()
    production_hours = models.IntegerField()

    def __str__(self) -> models.CharField:
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=32, null=True, blank=True)
    birth_date = models.DateField()
    job = models.ForeignKey(Job, on_delete=models.SET_NULL)
    passport = models.CharField(max_length=10)
    registration = models.TextField()
    department_id = models.IntegerField()
    work_phone_number = models.CharField(max_length=14)
    private_phone_number = models.CharField(max_length=14)

    def __str__(self) -> str:
        return f'{self.last_name} {self.first_name} {self.patronymic}'
