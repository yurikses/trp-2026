from pathlib import Path

from django.http import Http404
from django.shortcuts import render

from storage import load_data


def user_list(request):
    users = load_data(Path(__file__).resolve().parent.parent / 'data')['users']
    return render(request, 'users/list.html', {'users': list(users.values())})


def user_detail(request, user_id):
    data = load_data(Path(__file__).resolve().parent.parent / 'data')
    user = data['users'].get(user_id)
    if user is None:
        raise Http404('Пользователь не найден')
    return render(request, 'users/detail.html', {'user': user})

# Create your views here.
