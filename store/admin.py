from django.contrib import admin
from .models import Item, Category, Brand, Distributor, Image

class ItemImageInline(admin.TabularInline):
    model = Image
    extra = 3

class ItemAdmin(admin.ModelAdmin):
    inlines = [ ItemImageInline, ]

admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Distributor)
admin.site.register(Image)
