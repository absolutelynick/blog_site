from django.core.management.base import BaseCommand

from users.models import User
from api.constants.country_codes import COUNTRY_NAMES

from faker import Faker


def create_users_and_posts():
    # logger.info("Creating users")

    for i in range(20):
        faker = Faker()
        profile = faker.profile()

        first_name = profile["name"].split(" ")[0]
        last_name = profile["name"].split(" ")[1]
        username = f"{first_name}_{last_name}"

        email_domain = str(faker.email().split("@")[-1])
        email = f"{username.lower()}@{email_domain}"
        about = faker.text()

        fake_country = faker.country()
        country = fake_country if fake_country in COUNTRY_NAMES else "United Kingdom"

        date_of_birth = profile["birthdate"]
        website = profile["website"][0]
        gender = profile["sex"]

        User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            about=about,
            country=country,
            date_of_birth=date_of_birth,
            website=website,
            gender=gender,
        )


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_users_and_posts()
