from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse

class Category(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True)

    class MPTTMeta:
        unique_together = ('slug', 'parent',)
        verbose_name_plural = 'categories'
        order_insertion_by = ['name']

    def __str__(self):
        full_path = [self.name]
        ancestor = self.parent
        while ancestor is not None:
            full_path.append(ancestor.name)
            ancestor = ancestor.parent
        return ' -> '.join(full_path[::-1])

    def get_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
    photo = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Distributor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Item(models.Model):
    item_units = (
        (1, 'шт'),
        (2, 'м'),
        (3, 'пара'),
        (4, 'пог. м'),
        (5, 'кв. м'),
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True)
    units = models.IntegerField(choices=item_units, default=1)
    count = models.IntegerField()
    cost_price = models.IntegerField(default=0)
    retail_price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    distributor = models.ForeignKey(Distributor, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images', default=None)
    image = models.ImageField(upload_to='images/')
    is_main = models.BooleanField(null=True, default=None)

    def __str__(self):
        return self.image.url

class Characteristics(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='characteristics', default=None)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    