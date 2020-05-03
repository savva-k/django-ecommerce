from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings
from .models import Category, Item

def index(request):
    context = getCommonContext()
    return render(request, 'index.html', context)

def category(request, slug):
    context = getCommonContext()
    current_category = Category.objects.get(slug=slug)
    subcategories = list(map(lambda x: x.id, current_category.get_descendants(include_self=True)))
    items = Item.objects.filter(category__id__in=subcategories)
    paginator = Paginator(items, settings.ITEMS_PER_PAGE)
    page = resolve_page(request)
    context['current_category'] = current_category
    context['categories_ancestors'] = current_category.get_ancestors(include_self=True)
    context['items'] = paginator.get_page(page)
    context['page_range'] = paginator.page_range
    context['num_pages'] = paginator.num_pages
    context['currency_sign'] = settings.CURRENCY_SIGN
    return render(request, 'category.html', context)

def item(request, slug):
    context = getCommonContext()
    context['item'] = Item.objects.get(slug=slug)
    return render(request, 'item.html', context)

def getCommonContext():
    context = {}
    context['categories'] = Category.objects.all()
    context['variable'] = 'value1'
    return context

def resolve_page(request):
    page = request.GET.get('page')
    if (not (page is None) and str(page).isdigit()):
        return int(page)
    else:
        return 1
