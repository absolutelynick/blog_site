from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings

from api.constants.country_codes import COUNTRIES_ORDERED_DICT

import uuid, os, shutil
from datetime import datetime


BLOGPOST_MODEL = "blog.BlogPost"


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
        (GENDER_UNKNOWN, "Prefer not to say"),
    ]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(
        db_index=True, choices=GENDERS, default=GENDER_UNKNOWN, blank=True, max_length=1
    )
    date_of_birth = models.DateField(blank=True, null=True)

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    date_joined = models.DateTimeField("date joined", auto_now_add=True)
    date_modified = models.DateTimeField(
        "date modified", auto_now=True, null=True, blank=True
    )
    about = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)

    COUNTRY_UNKNOWN = "None"
    COUNTRY_NAMES_LIST = [("--", "None")] + COUNTRIES_ORDERED_DICT
    country = models.CharField(
        max_length=255, choices=COUNTRY_NAMES_LIST, default=COUNTRY_UNKNOWN, blank=True
    )

    picture_updated = models.DateTimeField(null=True)
    picture_file_path = models.CharField(max_length=128, null=True)
    picture_file_type = models.CharField(max_length=5, null=True)
    picture = models.ImageField(upload_to=picture_file_path, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    follows = models.ManyToManyField("self", related_name="follows", blank=True)
    followers = models.ManyToManyField("self", related_name="followers", blank=True)
    blocked = models.ManyToManyField("self", related_name="blocked", blank=True)

    posts = models.ManyToManyField(BLOGPOST_MODEL, related_name="posts", blank=True)
    liked = models.ManyToManyField(BLOGPOST_MODEL, related_name="liked", blank=True)
    comments = ArrayField(
        models.TextField(blank=False, null=False), blank=False, null=True
    )

    def __str__(self):
        return f"{self.username}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def profile_picture_path(self):
        return self.get_profile_picture_path()

    def get_profile_picture_path(self, file_type=None, raises=False):
        if (self.picture is None) or (os.path.exists(self.picture_file_path) == False):
            return os.path.join(settings.MEDIA_ROOT, "users/placeholder.png")

        return os.path.join(
            settings.USER_PICTURE_DIR,
            f"{str(self.uuid)}.{file_type or self.picture_file_type}",
        )

    @property
    def has_picture(self):
        return self.picture_file_type is not None

    def save_profile_pic(self, picture_file):
        file_type = picture_file.split(".")[-1]
        file_location = self.get_profile_picture_path(file_type)

        if settings.DEBUG:
            print(f"save_profile_pic: picture_file: {picture_file}")
            print(f"save_profile_pic: file_location: {file_location}")

        folder_location = os.path.dirname(file_location)
        if not os.path.exists(folder_location):
            os.makedirs(folder_location)

        with open(file_location, "wb") as f:
            shutil.copyfileobj(open(picture_file, "rb"), f)

        self.picture_updated = datetime.utcnow()
        self.picture_file_type = file_type
        self.picture_file_path = file_location
        self.picture = file_location

        self.save()

    def save(self, *args, **kwargs):
        self.date_modified = datetime.utcnow()
        super(User, self).save(*args, **kwargs)

    @property
    def fields(self):
        return {
            "First name": self.first_name,
            "Last name": self.last_name,
            "Gender": dict(self.GENDERS).get(
                str(self.date_of_birth), "Prefer not to say"
            ),
            "DOB": self.date_of_birth,
            "Username": self.username,
            "Email": self.email,
            "Date Joined": self.date_joined,
            "About": self.about,
            "Website": self.website,
        }

    class Meta(object):
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["last_name", "first_name"]
