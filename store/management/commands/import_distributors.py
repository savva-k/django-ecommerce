#!/usr/bin/env python
import csv
from django.core.management.base import BaseCommand, CommandError
from store.models import Distributor


class Command(BaseCommand):
    help = 'Import distributors from a CSV file. Warning: existing distributors will be overridden'

    def add_arguments(self, parser):
        parser.add_argument('--csv', help='A CSV with columns: id, name', required=True)

    def handle(self, *args, **options):
        with open(options['csv'], newline='') as file:
            distributors = csv.DictReader(file)
            for row in distributors:
                self.create_distributor(row['id'], row['name'])

    def create_distributor(self, id, name):
        self.stdout.write('Creating distributor: id=%s, name=%s' % (id, name))
        distributor = Distributor(id=int(id), name=name)
        distributor.save()
