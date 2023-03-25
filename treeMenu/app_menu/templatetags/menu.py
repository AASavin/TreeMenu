from django import template
from app_menu.models import MenuItem, Menu
from django.core.exceptions import ObjectDoesNotExist
from django.urls import resolve

register = template.Library()


@register.inclusion_tag('app_menu/menu.html', takes_context=True)
def draw_menu(context, menu):
    menu = Menu.objects.get(name=menu)
    current_url = context['request'].path
    oldest_items = MenuItem.objects.filter(menu=menu, parent=None)
    menu_items = [{'object': item, 'children': None} for item in oldest_items]
    try:
        active_item = MenuItem.objects.get(menu=menu, url=current_url)
    except ObjectDoesNotExist:
        try:
            named_url = resolve(context['request'].path_info).url_name
            active_item = MenuItem.objects.get(menu=menu, url=named_url)
        except ObjectDoesNotExist:
            return {'menu_items': menu_items}

    parents = active_item.get_parents()
    parents.append(active_item)
    menu_items = get_children(menu_items=menu_items, parents=parents)
    return {'menu_items': menu_items}


@register.inclusion_tag('app_menu/menu.html')
def print_children(item):
    return {'menu_items': item['children']}


def get_children(menu_items, parents):
    for item_id, item in enumerate(menu_items):
        if item['object'] == parents[0]:
            children = [{'object': child, 'children': None} for child in item['object'].children.all()]
            parents = parents[1:]
            if not parents:
                menu_items[item_id]['children'] = children
                return menu_items
            menu_items[item_id]['children'] = get_children(menu_items=children, parents=parents)
            return menu_items
