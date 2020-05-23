#!/usr/bin/env python
import csv
from django.core.management.base import BaseCommand, CommandError
from store.models import Brand


class Command(BaseCommand):
    help = 'Import brands from a CSV file. Warning: existing brands will be overridden'

    def add_arguments(self, parser):
        parser.add_argument('--csv',
                            help='A CSV with columns: id, name, photo, description',
                            required=True)

    def handle(self, *args, **options):
        with open(options['csv'], newline='') as file:
            brands = csv.DictReader(file)
            for row in brands:
                self.create_brand(row['id'], row['name'],
                                  row['photo'], row['description'])

    def create_brand(self, id, name, photo, description):
        self.stdout.write('Creating brand: id=%s, name=%s, photo=%s, description=%s'
                          % (id, name, photo, description))
        brand = Brand(id=int(id), name=name, photo=photo,
                      description=description)
        brand.save()
