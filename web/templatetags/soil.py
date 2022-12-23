from django import template

register = template.Library()


@register.inclusion_tag(r"web\form\form-in-view.html")
def filter_link(stage_form, names_to_select):
    return {"stage_form": stage_form, "names_to_select": names_to_select}
