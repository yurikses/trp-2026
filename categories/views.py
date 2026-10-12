from pathlib import Path

from django.http import Http404
from django.shortcuts import render

from storage import load_data


def category_list(request):
    data = load_data(Path(__file__).resolve().parent.parent / 'data')
    categories = list(data['categories'].values())
    return render(request, 'categories/list.html', {'categories': categories})


def category_detail(request, category_id):
    data = load_data(Path(__file__).resolve().parent.parent / 'data')
    category = data['categories'].get(category_id)
    if category is None:
        raise Http404('Категория не найдена')
    products = [item for item in data['products'].values() if item.category.id == category_id]
    return render(request, 'categories/detail.html', {'category': category, 'products': products})

# Create your views here.
