from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import MyUserManager


class User(AbstractBaseUser, PermissionsMixin):

    login = models.CharField(max_length=20, primary_key=True)
    id = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=50, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    registered_dttm = models.DateTimeField(auto_now_add=True, null=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'login'

    def __str__(self):
        return self.login

    def has_perm(self, perm, obj=None):
        if perm == "admin":
            return self.is_admin
        else:
            return True

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = '유저'
        verbose_name = '유저'
        verbose_name_plural = '유저'


class UserToken(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    ft_token = models.CharField(max_length=100, blank=True, null=True)
