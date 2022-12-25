import os.path

from django import template

from soil.settings import BASE_DIR

register = template.Library()


@register.inclusion_tag(os.path.join(BASE_DIR, r"web\templates\web\form\form-in-view.html"))
def filter_link(stage_form, names_to_select, prefix):
    return {
        "stage_form": stage_form,
        "names_to_select": names_to_select[0],
        "names_to_select_lat": names_to_select[1],
        "prefix": prefix,
    }
