from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from menu.views import menu_item_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('<path:slug>/', menu_item_view, name='menu_item'),
]
