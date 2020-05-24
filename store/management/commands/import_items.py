#!/usr/bin/env python
import csv
from django.core.management.base import BaseCommand, CommandError
from store.models import Item


class Command(BaseCommand):
    help = 'Import items from a CSV file. Warning: existing items will be overridden'

    item_units = {
        'шт': 1,
        'м': 2,
        'пара': 3,
        'пог. м': 4,
        'кв. м': 5,
        'комплект': 6,
        'упаковка': 7
    }

    def add_arguments(self, parser):
        parser.add_argument('--csv',
                            help='A CSV with columns: id, category, cost_price, ' +
                            'retail_price, name, distributor, description, brand, ' +
                            'country, seller, units, count',
                            required=True)

    def handle(self, *args, **options):
        with open(options['csv'], newline='') as file:
            items = csv.DictReader(file)
            for row in items:
                self.create_item(row['id'], row['category'], row['cost_price'], row['retail_price'],
                                 row['name'], row['distributor'], row['description'], row['brand'], row['country'],
                                 row['seller'], row['units'], row['count'])

    def create_item(self, id, category, cost_price, retail_price, name,
                    distributor, description, brand, country, seller, units, count):
        self.stdout.write('Creating category: id=%s, name=%s, count=%s, category=%s, cost_price=%s, retail_price=%s, brand=%s, distributor=%s, seller=%s'
                          % (id, name, count, category, cost_price, retail_price, brand, distributor, seller))
        
        category = self.to_int_or_none(category)
        count = self.to_int_or_none(count)
        cost_price = self.to_int_or_none(cost_price)
        retail_price = self.to_int_or_none(retail_price)
        brand = self.to_int_or_none(brand)
        distributor = self.to_int_or_none(distributor)
        seller = self.to_int_or_none(seller)

        item = Item(id=int(id), category_id=category, units=self.item_units[units], name=name, count=count, cost_price=cost_price,
                    retail_price=retail_price, brand_id=brand, distributor_id=distributor, description=description, madeIn=country, seller_id=seller)
        item.save()
    
    def to_int_or_none(self, maybe_numeber):
        try:
            return int(maybe_numeber)
        except ValueError:
            return None