#!/usr/bin/env python
import csv
from django.core.management.base import BaseCommand, CommandError
from store.models import Seller


class Command(BaseCommand):
    help = 'Import sellers from a CSV file. Warning: existing sellers will be overridden'

    def add_arguments(self, parser):
        parser.add_argument('--csv', help='A CSV with columns: id, name', required=True)

    def handle(self, *args, **options):
        with open(options['csv'], newline='') as file:
            sellers = csv.DictReader(file)
            for row in sellers:
                self.create_seller(row['id'], row['name'])

    def create_seller(self, id, name):
        self.stdout.write('Creating seller: id=%s, name=%s' % (id, name))
        seller = Seller(id=int(id), name=name)
        seller.save()
