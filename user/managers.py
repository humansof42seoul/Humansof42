from django.contrib.auth.models import BaseUserManager
from .ftauth import get_random_string

class MyUserManager(BaseUserManager):
    def create_user(self, id, email, username):
        user = self.model(
            id=id,
            email=email,
            username=username,
        )
        user.is_admin = False
        user.is_active = True
        user.set_password(username)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def is_staff(self):
        return self.is_admin
