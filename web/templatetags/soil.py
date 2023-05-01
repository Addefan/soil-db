from pathlib import Path

from django import template

register = template.Library()


def queryset_names(names_to_select, var):
    ans = []
    for obj in names_to_select:
        ans.append(getattr(obj, var))
    return ans


@register.inclusion_tag(Path("web") / "form" / "form-in-view.html")
def suggestions(stage_form, names_to_select):
    taxonomy = {}
    for level in ("phylum", "class", "order", "family", "genus"):
        for attr in ("title", "latin_title"):
            taxonomy[f"{level}_{attr}"] = queryset_names(names_to_select[level], attr)
    return {"form": stage_form, "taxonomy": taxonomy}


@register.filter(name="getattr")
def get_attr(obj, attr_name):
    """Try to get an attribute from an object.

    Example: {% if block|getattr:"editable" %}
    """
    try:
        return obj.get(attr_name) or obj.__getattribute__(attr_name)
    except AttributeError:
        return None


@register.inclusion_tag(Path("web") / "snippets" / "toast.html")
def toast(toast_id, message_header, text_color_class, message_text):
    return {
        "toast_id": toast_id,
        "message_header": message_header,
        "text_color_class": text_color_class,
        "message_text": message_text,
    }
