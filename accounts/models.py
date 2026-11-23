from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Manager for a user model that logs in with an e-mail address instead of a username."""

    use_in_migrations = True

    @classmethod
    def normalize_email(cls, email):
        # Treat e-mail addresses case-insensitively, so Jan@Example.com == jan@example.com.
        return (email or '').strip().lower()

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The e-mail address must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """RentOven user account. Customers sign in with their e-mail address and password."""

    username = None
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={'unique': 'A user with this e-mail address already exists.'},
    )
    first_name = models.CharField('first name', max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['email']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.__class__.objects.normalize_email(self.email)
        super().save(*args, **kwargs)
