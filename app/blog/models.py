from django.db import models
from django.contrib.postgres.fields import ArrayField

import uuid
from datetime import datetime

USERS_MODEL = "users.User"


class BlogPost(models.Model):
    title = models.CharField(max_length=155)
    slug = models.SlugField(max_length=50, null=True, unique=True)
    content = models.TextField(null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    liked_by = models.ManyToManyField(USERS_MODEL, blank=True)
    hashtags = ArrayField(
        models.TextField(blank=True, null=False), blank=True, null=True
    )
    posted_by = models.ForeignKey(
        USERS_MODEL, null=True, related_name="author", on_delete=models.SET_NULL
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.posted_by}"

    @property
    def post(self):
        return f"{self.first_name} {self.last_name}"

    class Meta(object):
        ordering = ["title"]
        unique_together = ("title", "posted_by")


class Comment(models.Model):
    post = models.ForeignKey(
        BlogPost, null=True, related_name="BlogPost", on_delete=models.SET_NULL
    )
    comment = models.TextField(max_length=256, null=True, blank=True)
    comment_by = models.ForeignKey(
        USERS_MODEL, null=True, related_name="user", on_delete=models.SET_NULL
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    @property
    def username(self):
        return self.comment_by.username

    @property
    def email(self):
        return self.comment_by.email

    class Meta:
        ordering = ("date_created",)

    def __str__(self):
        return f"Comment by '{self.comment_by.username}' on '{self.post}'"

    def save(self, *args, **kwargs):
        self.date_modified = datetime.utcnow()
        super(Comment, self).save(*args, **kwargs)
