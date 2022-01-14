from django.contrib.auth.models import BaseUserManager
from .ftauth import get_random_string

<<<<<<< HEAD
class MyUserManager(BaseUserManager):
=======
class MyUserManager(BaseUserManager)
>>>>>>> 3850fdca24022db98f0943c0a2907c2d82abacb2
    def create_user(self, id, email, login):
        user = self.model(
            id=id,
            email=email,
            login=login,
        )
        user.is_admin = False
        user.is_active = True
        user.set_password(login)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password):
        user = self.model(
            login=login,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def is_staff(self):
        return self.is_admin
