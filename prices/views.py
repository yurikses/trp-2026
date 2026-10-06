from html import escape
from pathlib import Path

from django.http import HttpResponse

from home.views import render_page
from storage import load_data


def price_list(request):
	prices = load_data(Path(__file__).resolve().parent.parent / 'data')['prices']
	items = ''.join(
		f'<li class="list-group-item"><a href="/prices/{index}/">'
		f'{escape(item.product.name)} в {escape(item.store.name)}</a>'
		f'<span class="float-end">{item.price:,.2f} ₽</span></li>'
		for index, item in enumerate(prices, 1)
	)
	return render_page('Цены', f'<h1 class="mb-4">Цены</h1><ul class="list-group">{items}</ul>')


def price_detail(request, price_id):
	prices = load_data(Path(__file__).resolve().parent.parent / 'data')['prices']
	if price_id < 1 or price_id > len(prices):
		return HttpResponse('Цена не найдена', status=404)
	item = prices[price_id - 1]
	content = f'''<div class="card"><div class="card-body">
	  <h1 class="h3">{escape(item.product.name)}</h1>
	  <p class="fs-3">{item.price:,.2f} ₽</p>
	  <p>Магазин: <a href="/stores/{item.store.id}/">{escape(item.store.name)}</a></p>
	  <p>Обновлено: {item.updated_at:%d.%m.%Y %H:%M}</p>
	  <a class="btn btn-primary" href="{escape(item.url)}">Перейти к предложению</a>
	</div></div>'''
	return render_page('Цена', content)

# Create your views here.
