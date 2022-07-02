import codecs
import csv
import os
from os.path import exists

from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR
from reviews.models import Category, Title, Genre, Review, Comment, GenreTitle
from users.models import User

MAPPING = (
    (User, 'users.csv'),
    (Category, 'category.csv'),
    (Genre, 'genre.csv'),
    (Title, 'titles.csv'),
    (GenreTitle, 'genre_title.csv'),
    (Review, 'review.csv'),
    (Comment, 'comments.csv'),
)
CSV_DIR_PATH = os.path.join(BASE_DIR, 'static/data')


class Command(BaseCommand):
    help = 'Импортирует данные в БД из csv файлов'

    def handle(self, *args, **options):
        for row in MAPPING:
            self.import_from_csv(row[0], row[1])

    def import_from_csv(self, model_name, file_name):
        full_path = CSV_DIR_PATH + '/' + file_name
        if not exists(full_path):
            self.stdout.write(
                self.style.ERROR(f'File {full_path} not exist!'))
            return False

        created_counter = 0
        updated_counter = 0
        error_counter = 0
        self.stdout.write(self.style.NOTICE(
            f'Start import from {file_name}'
        ))

        with codecs.open(full_path, "r", "utf_8_sig") as f:
            reader = csv.reader(f)
            fields_names = False
            for row in reader:
                if not fields_names:
                    fields_names = row
                    continue

                try:
                    obj, created = model_name.objects.get_or_create(
                        **dict(zip(fields_names, row)))
                    if created:
                        created_counter += 1
                    else:
                        updated_counter += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(
                        f'Can t import row {str(row)} '
                        f'to model {model_name.__name__}: {e}'))
                    error_counter += 1

        self.stdout.write(self.style.SUCCESS(
            f'Created: {created_counter}   '
            f'Updated: {updated_counter}   '
            f'Errors: {error_counter}'
        ))
