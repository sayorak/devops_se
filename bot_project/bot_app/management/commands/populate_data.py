from django.core.management.base import BaseCommand
from faker import Faker
import random
from bot_app.models import Author, Book, Review

class Command(BaseCommand):
    help = 'Populates the database with random data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Authors
        authors = []
        for _ in range(10):
            authors.append(Author(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                birth_date=fake.date_of_birth(minimum_age=20, maximum_age=70),
            ))
        Author.objects.bulk_create(authors)

        # Create Books
        books = []
        for _ in range(10):
            books.append(Book(
                title=fake.sentence(nb_words=4),
                author=random.choice(authors),
                published_date=fake.date_between(start_date='-10y', end_date='today'),
                isbn=fake.isbn13(separator=""),
                price=round(random.uniform(10.0, 100.0), 2),
            ))
        Book.objects.bulk_create(books)

        # Create Reviews
        reviews = []
        for _ in range(10):
            reviews.append(Review(
                book=random.choice(books),
                reviewer_name=fake.name(),
                rating=random.randint(1, 5),
                comment=fake.paragraph(nb_sentences=3),
            ))
        Review.objects.bulk_create(reviews)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
