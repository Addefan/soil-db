from pathlib import Path

from django import template

register = template.Library()


@register.inclusion_tag(Path("web") / "form" / "form-in-view.html")
def suggestions(stage_form, taxon_levels):
    taxonomy = {}
    for taxon_level in taxon_levels:
        taxonomy[f"{taxon_level['level']}_title"] = taxon_level["titles"]
        taxonomy[f"{taxon_level['level']}_latin_title"] = taxon_level["latin_titles"]
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
