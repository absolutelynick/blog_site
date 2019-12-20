from django.db import models
from django.contrib.postgres.fields import ArrayField

import uuid

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
        USERS_MODEL, null=True, related_name="owner", on_delete=models.SET_NULL
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
