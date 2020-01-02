from django.core.management.base import BaseCommand

from users.models import User
from blog.models import BlogPost

from faker import Faker
import random


def create_users_and_posts():
    users = User.objects.all()

    for i in range(5):
        user = users[random.randint(0, (len(users)) - 1)]

        for num in range(5):
            faker_post = Faker()

            title = faker_post.sentence(nb_words=random.randint(1, 5))
            slug = title.replace(" ", "_")
            content = faker_post.paragraph(nb_sentences=random.randint(1, 10))

            BlogPost.objects.create(
                title=title, slug=slug, content=content, posted_by=user
            )


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_users_and_posts()
