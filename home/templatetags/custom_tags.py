from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def check_page_param(value):
    value_list = value.split('&')
    if "page=" in value_list[0]:
        value_list.pop(0)
        return f'{"&".join(value_list)}'
    
    return value

@register.filter
def wrap_string(value, length=20):
    wrapped_text = '<br>'.join([value[i:i+length] for i in range(0, len(value), length)])
    return mark_safe(wrapped_text)

@register.filter
def is_empty_values(elements):
    for element in elements:
        if element["value"] != '':
            return False
    return True

@register.filter
def replace_characters(value, chars):
    chars_list = [char.strip() for char in chars.split('&')]
    return str(value).replace(chars_list[0], chars_list[1])

@register.filter
def divide(value, arg):
    try:
        return round(float(value) / float(arg), 3)
    except (ValueError, ZeroDivisionError):
        return None
    
@register.filter
def get_full_name_group_and_wrap(value, for_mobile=False):
    if for_mobile:
        return f'{value.last_name} {value.first_name} {value.patronymic if value.patronymic else ""} ({value.group})'
    return wrap_string(f'{value.last_name} {value.first_name} {value.patronymic if value.patronymic else ""} ({value.group})')
    #return wrap_string(f'<b>{value.group}: </b>{value.last_name} {value.first_name} {value.patronymic if value.patronymic else ""}')