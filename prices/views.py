from pathlib import Path

from django.http import Http404
from django.shortcuts import render

from storage import load_data


def price_list(request):
    prices = load_data(Path(__file__).resolve().parent.parent / 'data')['prices']
    return render(request, 'prices/list.html', {'prices': prices})


def price_detail(request, price_id):
    prices = load_data(Path(__file__).resolve().parent.parent / 'data')['prices']
    if price_id < 1 or price_id > len(prices):
        raise Http404('Цена не найдена')
    item = prices[price_id - 1]
    return render(request, 'prices/detail.html', {'price': item})

# Create your views here.
