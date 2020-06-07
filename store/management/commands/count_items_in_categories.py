#!/usr/bin/env python
from django.core.management.base import BaseCommand, CommandError
from store.models import Item, Category


class Command(BaseCommand):
    help = 'Counts items in categories and saves the numbers in the DB'

    def handle(self, *args, **options):
        categories = Category.objects.all()

        for current_category in categories:
            subcategories = list(map(lambda x: x.id, current_category.get_descendants(include_self=True)))
            items_number = Item.objects.filter(category__id__in=subcategories).count()
            current_category.number_of_items = items_number
            current_category.save()
            self.stdout.write('%s -> %s items' % (current_category, items_number))
