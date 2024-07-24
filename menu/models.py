from django.db import models
from django.urls import reverse


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
