from django.db import models
from django.db import models
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager,
)


class UserManager(BaseUserManager):
    user_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set(required True)')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True. ')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True. ')
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    password = models.CharField(max_length=100)
    activation_code = models.CharField(max_length=100)
    objects = UserManager()
    username = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def activate_with_code(self, code):
        if str(self.activation_code) != str(code):
            raise Exception('Code does not match')
        self.is_active = True
        self.activation_code = ''
        self.save(update_fields=['is_active', 'activation_code'])

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code
        self.save(update_fields=['activation_code'])


        # get_random_string(length=6,allowed_chars='0123456789ABC...abc...') генерит рандомный код активации для смс
        # на телефон