from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=155)
    content = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=50, null=True, unique=True)

    def __str__(self):
        return self.title
