from django.shortcuts import render
from .models import Category, Item

def index(request):
    context = getCommonContext()
    return render(request, 'index.html', context)

def category(request, slug):
    context = getCommonContext()
    current_category = Category.objects.get(slug=slug)
    subcategories = list(map(lambda x: x.id, current_category.get_descendants(include_self=True)))
    context['current_category'] = current_category
    context['categories_ancestors'] = current_category.get_ancestors(include_self=True)
    context['items'] = Item.objects.filter(category__id__in=subcategories)
    return render(request, 'category.html', context)

def getCommonContext():
    context = {}
    context['categories'] = Category.objects.all()
    context['variable'] = 'value1'
    return context