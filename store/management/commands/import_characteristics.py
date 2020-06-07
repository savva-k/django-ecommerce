#!/usr/bin/env python
import csv
from django.core.management.base import BaseCommand, CommandError
from store.models import Characteristics, Item


class Command(BaseCommand):
    help = 'Import characteristics from a CSV file. Warning: existing characteristics will be overridden'

    def add_arguments(self, parser):
        parser.add_argument('--csv', help='A CSV with columns: id, item_id, key, value', required=True)

    def handle(self, *args, **options):
        with open(options['csv'], newline='') as file:
            characteristics = csv.DictReader(file)
            for row in characteristics:
                self.create_characteristics(row['id'], row['item_id'], row['key'], row['value'])

    def create_characteristics(self, id, item_id, key, value):
        self.stdout.write('Creating characteristics: item_id=%s, key=%s value=%s' % (item_id, key, value))
        
        if Item.objects.filter(pk=item_id).exists():
            characteristics = Characteristics(id=id, item_id=item_id, key=key, value=value)
            characteristics.save()
