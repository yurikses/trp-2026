from html import escape
from pathlib import Path

from django.http import HttpResponse

from home.views import render_page
from storage import load_data


def store_list(request):
    stores = load_data(Path(__file__).resolve().parent.parent / 'data')['stores']
    items = ''.join(
        f'<li class="list-group-item"><a href="/stores/{item.id}/">{escape(item.name)}</a>'
        f'<small class="d-block text-muted">{escape(item.url)}</small></li>'
        for item in stores.values()
    )
    return render_page('Магазины', f'<h1 class="mb-4">Магазины</h1><ul class="list-group">{items}</ul>')


def store_detail(request, store_id):
    data = load_data(Path(__file__).resolve().parent.parent / 'data')
    store = data['stores'].get(store_id)
    if store is None:
        return HttpResponse('Магазин не найден', status=404)
    prices = [item for item in data['prices'] if item.store.id == store_id]
    cards = ''.join(
        f'<div class="col-md-6"><div class="card"><div class="card-body">'
        f'<h2 class="h5">{escape(item.product.name)}</h2><p>{item.price:,.2f} ₽</p></div></div></div>'
        for item in prices
    ) or '<p class="text-muted">Предложения не найдены.</p>'
    content = f'<div class="card mb-4"><div class="card-body"><h1>{escape(store.name)}</h1>'
    content += f'<a href="{escape(store.url)}">{escape(store.url)}</a></div></div>'
    return render_page('Магазин', content + '<h2 class="h4 mb-3">Предложения</h2><div class="row g-3">'
                       + cards + '</div>')

# Create your views here.
