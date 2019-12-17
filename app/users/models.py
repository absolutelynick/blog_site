from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.contrib import auth

from django.db import models
import uuid


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(first_name, last_name, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    objects = UserManager()

    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_UNKNOWN = "U"

    GENDERS = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_UNKNOWN, "Unknown"),
    ]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(
        db_index=True, choices=GENDERS, default=GENDER_UNKNOWN, blank=True, max_length=1
    )

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    date_joined = models.DateTimeField("date joined", auto_now_add=True)
    date_modified = models.DateTimeField(
        "date modified", auto_now=True, null=True, blank=True
    )
    picture_updated = models.DateTimeField(null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"@{self.username}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta(object):
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["last_name", "first_name"]
