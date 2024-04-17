from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    
    def create_user(self, full_name, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            full_name=full_name,
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, username, email, password):
        user = self.create_user(
            full_name,
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user