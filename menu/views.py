from django.shortcuts import render, get_object_or_404

from .models import MenuItem


def menu_item_view(request, slug):
    slugs = slug.split('/')
    menu_item = get_object_or_404(MenuItem, slug=slugs[-1])  # Получаем последний пункт меню
    return render(request, 'home.html', {'menu_item': menu_item})
