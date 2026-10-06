from html import escape
from pathlib import Path

from django.http import HttpResponse

from home.views import render_page
from storage import load_data


def category_list(request):
    categories = load_data(Path(__file__).resolve().parent.parent / 'data')['categories']
    items = ''.join(
        f'<li class="list-group-item"><a href="/categories/{item.id}/">'
        f'{escape(item.name)}</a></li>' for item in categories.values()
    )
    return render_page('Категории', f'<h1 class="mb-4">Категории</h1><ul class="list-group">{items}</ul>')


def category_detail(request, category_id):
    data = load_data(Path(__file__).resolve().parent.parent / 'data')
    category = data['categories'].get(category_id)
    if category is None:
        return HttpResponse('Категория не найдена', status=404)
    products = [item for item in data['products'].values() if item.category.id == category_id]
    related = ''.join(
        f'<li class="list-group-item"><a href="/products/{item.id}/">{escape(item.name)}</a></li>'
        for item in products
    ) or '<li class="list-group-item">Товаров пока нет</li>'
    content = f'<div class="card"><div class="card-body"><h1>{escape(category.name)}</h1>'
    content += f'<p class="text-muted">ID: {category.id}</p><h2 class="h5">Товары</h2>'
    return render_page('Категория', content + f'<ul class="list-group">{related}</ul></div></div>')

# Create your views here.
