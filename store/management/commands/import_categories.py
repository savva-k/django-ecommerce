#!/usr/bin/env python
import csv
from django.core.management.base import BaseCommand, CommandError
from store.models import Category


class Command(BaseCommand):
    help = 'Import categories from a CSV file. Warning: existing categories will be overridden'

    def add_arguments(self, parser):
        parser.add_argument('--csv',
                            help='A CSV with columns: id, parent_id, category_name',
                            required=True)

    def handle(self, *args, **options):
        with open(options['csv'], newline='') as file:
            categories = csv.DictReader(file)
            for row in categories:
                self.create_category(row['id'], row['parent'], row['name'])

    def create_category(self, id, parent, name):
        self.stdout.write(
            'Creating category: id=%s, parent_id=%s, name=%s' % (id, parent, name))
        parent_id = None if parent == "0" else int(parent)
        category = Category(id=int(id), parent_id=parent_id, name=name)
        category.save()
