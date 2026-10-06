from html import escape
from pathlib import Path

from django.http import HttpResponse

from home.views import render_page
from storage import load_data


def product_list(request):
    products = load_data(Path(__file__).resolve().parent.parent / 'data')['products']
    items = ''.join(
        f'<li class="list-group-item d-flex justify-content-between"><a href="/products/{item.id}/">'
        f'{escape(item.name)}</a><span class="badge text-bg-secondary">{escape(item.category.name)}</span></li>'
        for item in products.values()
    )
    return render_page('Товары', f'<h1 class="mb-4">Товары</h1><ul class="list-group">{items}</ul>')


def product_detail(request, product_id):
    data = load_data(Path(__file__).resolve().parent.parent / 'data')
    product = data['products'].get(product_id)
    if product is None:
        return HttpResponse('Товар не найден', status=404)
    prices = [item for item in data['prices'] if item.product.id == product_id]
    cards = ''.join(
        f'<div class="col-md-6"><div class="card h-100"><div class="card-body">'
        f'<h3 class="h5">{escape(item.store.name)}</h3><p class="fs-4">{item.price:,.2f} ₽</p>'
        f'<a href="{escape(item.url)}" class="btn btn-outline-primary">Открыть магазин</a>'
        '</div></div></div>' for item in prices
    ) or '<p class="text-muted">Цены не найдены.</p>'
    content = f'<div class="card mb-4"><div class="card-body"><h1>{escape(product.name)}</h1>'
    content += f'<p>{escape(product.description) or "Описание отсутствует."}</p>'
    content += f'<p class="text-muted">Категория: {escape(product.category.name)}</p></div></div>'
    return render_page('Товар', content + '<h2 class="h4 mb-3">Предложения</h2><div class="row g-3">'
                       + cards + '</div>')

# Create your views here.
