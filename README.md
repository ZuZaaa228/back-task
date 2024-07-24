# Установка и запуск

```bash
git clone https://github.com/ZuZaaa228/back-task.git 
cd back-task
pip install django
python manage.py runserver
```

> Данные меню уже есть в БД

## Доступ к админке
username: root
password: 1
```
http://127.0.0.1:8000/admin/
```

### Увидеть меню можно по адресу
```
http://127.0.0.1:8000/
```

# Реализация

 1. template tag:
```python
# menu/templatetags/menu_tags.py
@register.inclusion_tag('menu/menu.html', takes_context=True)  
def draw_menu(context, menu_name):  
    request = context['request']  
    current_path = request.path  
    menu_items = get_menu_items(menu_name, current_path)  
    return {'menu_items': menu_items, 'current_path': current_path}
```
2. Все, что было выбрано доступно для отображения и выделяется в файле: ```
templates/menu/menu.html ```
А также для получения всех выбранных раннее пунктов используется функция ```get_menu_items(menu_name, current_path)``` из ``` menu/templatetags/menu_tags.py```
3. Меню хранится в БД в виде следующей модели:
```python
# menu/models.py
class MenuItem(models.Model):  
    name = models.CharField(max_length=100)  
    slug = models.SlugField(unique=True)  
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)  
    url = models.CharField(max_length=200, blank=True)  
    named_url = models.CharField(max_length=200, blank=True)  
    menu_name = models.CharField(max_length=100)  
  
    def get_absolute_url(self):  
        slugs = []  
        item = self  
 while item:  
            slugs.insert(0, item.slug)  
            item = item.parent  
        return reverse('menu_item', kwargs={'slug': '/'.join(slugs)})  
  
    def __str__(self):  
        return self.name
```
4. Редактирование в стандартной Django-админ панели: ```menu/admin.py```
5. Активный пункт определяется исходя из url страницы: 
```jinja2
...
	<a href="{{ node.item.get_absolute_url }}"  
	class="{% if node.item.get_absolute_url == current_path %}active{% endif %}">{{ node.item.name }}</a>
...
	<a href="{{ child.item.get_absolute_url }}"  
	class="{% if child.item.get_absolute_url == current_path %}active{% endif %}">{{ child.item.name }}</a>
...
```
Остальной код находится в ```menu/templatetags/menu_tags.py```.

6. На 1 страницу можно поместить несколько меню, определяются по названию: 
```jinja2
...
<div>  
    <h2>Main Menu</h2>  
    {% draw_menu 'main_menu' %}  
</div>  
  
<div>  
    <h2>Secondary Menu</h2>  
    {% draw_menu 'secondary_menu' %}  
</div>
...
```
Остальной код шаблона с двумя меню в ```templates/home.html```.
7. При клике будет выполнен переход на url пункта из меню:
```python
# menu/views.py
def menu_item_view(request, slug):  
    slugs = slug.split('/')  
    menu_item = get_object_or_404(MenuItem, slug=slugs[-1])  # Получаем последний пункт меню  
  return render(request, 'home.html', {'menu_item': menu_item})
```
```python
# taskMenu/urls.py
urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('', TemplateView.as_view(template_name='home.html'), name='home'),  
    path('<path:slug>/', menu_item_view, name='menu_item'),  
]
```
8. На отрисовку используется 1 запрос: 
Можно использовать такой код:
```python
class MenuTests(TestCase):  
  
    def test_menu_renders_with_one_query(self):  
      """  
         Проверка на количество запросов к базе данных  :return:  
      """
      client = Client()  
        with CaptureQueriesContext(connection) as queries:  
            client.get("/home/about/team/member-1/")  
            client.get("/home/about/team/member-2/")  
            client.get("/home/about/team/member-1/")  
            client.get("/home/about/team/")  
            client.get("/home/about/history/")  
            client.get("/home/services/")  
            client.get("/")  # Тут даст 2 запроса, т.к рендерит 2 меню: main_menu, secondary_menu  
  
  print(f"SQL queries: {len(queries)}")  
        self.assertEqual(len(queries), 8)
```
Для тестирования количества запросов к БД. 


