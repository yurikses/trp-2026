from html import escape

from django.http import HttpResponse


def render_page(title: str, content: str) -> HttpResponse:
		"""Возвращает общий HTML-каркас веб-интерфейса проекта."""
		html = f"""<!doctype html>
<html lang="ru">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>{escape(title)} | Rubdiff</title>
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
	<nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
		<div class="container">
			<a class="navbar-brand fw-bold" href="/">Rubdiff</a>
			<div class="navbar-nav">
				<a class="nav-link" href="/products/">Товары</a>
				<a class="nav-link" href="/categories/">Категории</a>
				<a class="nav-link" href="/stores/">Магазины</a>
				<a class="nav-link" href="/prices/">Цены</a>
				<a class="nav-link" href="/users/">Пользователи</a>
			</div>
		</div>
	</nav>
	<main class="container pb-5">{content}</main>
</body>
</html>"""
		return HttpResponse(html)


def home(request):
		content = """
		<div class="p-5 mb-4 bg-white rounded-3 shadow-sm">
			<h1 class="display-5 fw-bold">Сравнение цен без лишнего поиска</h1>
			<p class="lead">Rubdiff собирает предложения магазинов и помогает найти лучшую цену.</p>
			<a class="btn btn-primary btn-lg" href="/products/">Перейти к товарам</a>
		</div>
		<div class="row g-3">
			<div class="col-md-4"><div class="card h-100"><div class="card-body">
				<h2 class="h5">Каталог</h2><p class="mb-0">Товары и их категории.</p>
			</div></div></div>
			<div class="col-md-4"><div class="card h-100"><div class="card-body">
				<h2 class="h5">Магазины</h2><p class="mb-0">Источники актуальных предложений.</p>
			</div></div></div>
			<div class="col-md-4"><div class="card h-100"><div class="card-body">
				<h2 class="h5">Сравнение</h2><p class="mb-0">Цены отсортированы от меньшей к большей.</p>
			</div></div></div>
		</div>
		"""
		return render_page("Главная", content)

# Create your views here.
