from html import escape
from pathlib import Path

from django.http import HttpResponse

from home.views import render_page
from storage import load_data


def user_list(request):
	users = load_data(Path(__file__).resolve().parent.parent / 'data')['users']
	items = ''.join(
		f'<li class="list-group-item"><a href="/users/{item.id}/">{escape(item.name)}</a>'
		f'<span class="text-muted">{escape(item.email)}</span></li>'
		for item in users.values()
	)
	return render_page('Пользователи', f'<h1 class="mb-4">Пользователи</h1><ul class="list-group">{items}</ul>')


def user_detail(request, user_id):
	data = load_data(Path(__file__).resolve().parent.parent / 'data')
	user = data['users'].get(user_id)
	if user is None:
		return HttpResponse('Пользователь не найден', status=404)
	favorites = ''.join(
		f'<li class="list-group-item"><a href="/products/{item.id}/">{escape(item.name)}</a></li>'
		for item in user.favorites
	) or '<li class="list-group-item">Избранное пусто</li>'
	content = f'<div class="card"><div class="card-body"><h1>{escape(user.name)}</h1>'
	content += f'<p><a href="mailto:{escape(user.email)}">{escape(user.email)}</a></p>'
	content += f'<h2 class="h5">Избранные товары</h2><ul class="list-group">{favorites}</ul>'
	return render_page('Пользователь', content + '</div></div>')

# Create your views here.
