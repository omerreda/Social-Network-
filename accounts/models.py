from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, gender, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Must have username')

        if len(password) < 8:
            raise ValueError('Password Must be over 8 Char')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, gender, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            username,
            first_name,
            last_name,
            gender,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'


class NewUser(AbstractBaseUser):
    class GENDER(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=125,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Username must be alpahnmeric or contain any of the following: ". @ + -"',
                code='invalid_username'
            ),
        ],
        unique=True
    )
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    country = models.CharField(max_length=125, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER.choices)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'gender']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True