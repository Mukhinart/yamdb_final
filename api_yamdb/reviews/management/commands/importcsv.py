# Пример запроса для загрузки данных: python manage.py
# importcsv --path static/data/category.csv --mod Category --app reviews

import csv

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создание объектов для выбранной модели'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='путь к файлу')
        parser.add_argument(
            '--model_name', '--mod',
            type=str,
            help='название модели'
        )
        parser.add_argument(
            '--app_name', '--app',
            type=str,
            help='приложение, в котором находится модель'
        )

    def handle(self, *args, **options):
        file_path = options['path']
        _model = apps.get_model(options['app_name'], options['model_name'])
        with open(file_path, 'rt', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            header = next(reader)
            for row in reader:
                _object_dict = {key: value for key, value in zip(header, row)}
                _model.objects.create(**_object_dict)
