from django.db import models
import uuid


class BlogPost(models.Model):
    title = models.CharField(max_length=155)
    slug = models.SlugField(max_length=50, null=True, unique=True)
    content = models.TextField(null=True, blank=True, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
