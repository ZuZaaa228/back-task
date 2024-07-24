from django import template

from menu.models import MenuItem

register = template.Library()


def get_menu_items(menu_name, current_path):
    def build_tree(parent):
        children = items_by_parent.get(parent.id, [])
        node = {'item': parent, 'children': []}
        for child in children:
            node['children'].append(build_tree(child))
        return node

    items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent').order_by('id')
    items_by_parent = {}
    for item in items:
        items_by_parent.setdefault(item.parent_id, []).append(item)

    roots = items_by_parent.get(None, [])
    tree = [build_tree(root) for root in roots]

    def expand_tree(nodes):
        for node in nodes:
            node['expanded'] = node['item'].get_absolute_url() in current_path
            if node['expanded']:
                expand_tree(node['children'])

    expand_tree(tree)

    return tree


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path
    menu_items = get_menu_items(menu_name, current_path)
    return {'menu_items': menu_items, 'current_path': current_path}
