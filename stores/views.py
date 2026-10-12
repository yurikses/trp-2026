from pathlib import Path

from django.http import Http404
from django.shortcuts import render

from storage import load_data


def store_list(request):
    data = load_data(Path(__file__).resolve().parent.parent / 'data')
    stores = list(data['stores'].values())
    return render(request, 'stores/list.html', {'stores': stores})


def store_detail(request, store_id):
    data = load_data(Path(__file__).resolve().parent.parent / 'data')
    store = data['stores'].get(store_id)
    if store is None:
        raise Http404('Магазин не найден')
    prices = [item for item in data['prices'] if item.store.id == store_id]
    return render(request, 'stores/detail.html', {'store': store, 'prices': prices})

# Create your views here.
