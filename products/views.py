from pathlib import Path

from django.http import Http404
from django.shortcuts import render

from storage import load_data


def product_list(request):
    data = load_data(Path(__file__).resolve().parent.parent / 'data')
    products = list(data['products'].values())
    return render(request, 'products/list.html', {'products': products})


def product_detail(request, product_id):
    data = load_data(Path(__file__).resolve().parent.parent / 'data')
    product = data['products'].get(product_id)
    if product is None:
        raise Http404('Товар не найден')
    prices = [item for item in data['prices'] if item.product.id == product_id]
    return render(request, 'products/detail.html', {'product': product, 'prices': prices})

# Create your views here.
