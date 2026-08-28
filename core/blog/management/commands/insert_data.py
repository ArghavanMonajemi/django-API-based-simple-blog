from django.core.management.base import BaseCommand
from faker import Faker
from account.models import User, Profile
from blog.models import Category, Post
import random
from datetime import datetime

category_list = ["fun", "food", "travel", "tech"]


class Command(BaseCommand):
    help = "Create fake data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **kwargs):
        user = User.objects.create_user(email=self.faker.email(), password="test@12345")
        profile = Profile.objects.get(user=user)
        profile.first_name = self.faker.first_name()
        profile.last_name = self.faker.last_name()
        profile.bio = self.faker.paragraph(nb_sentences=3)
        profile.save()
        for name in category_list:
            Category.objects.get_or_create(name=name)
        for _ in range(10):
            Post.objects.create(
                author=profile,
                title=self.faker.sentence(nb_words=3),
                content=self.faker.paragraph(),
                category=Category.objects.get(name=random.choice(category_list)),
                status=random.choice([True, False]),
                pub_date=datetime.now(),
            )
