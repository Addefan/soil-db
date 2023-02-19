import os.path

from django import template

register = template.Library()


def queryset_names(names_to_select, var):
    ans = []
    for obj in names_to_select:
        ans.append(getattr(obj, var))
    return ans


@register.inclusion_tag(os.path.join("web", "form", "form-in-view.html"))
def suggestions(stage_form, names_to_select):
    return {
        "stage_form": stage_form,
        "phylum_title": queryset_names(names_to_select["phylum"], "title"),
        "phylum_latin_title": queryset_names(names_to_select["phylum"], "latin_title"),
        "class_title": queryset_names(names_to_select["class"], "title"),
        "class_latin_title": queryset_names(names_to_select["class"], "latin_title"),
        "order_title": queryset_names(names_to_select["order"], "title"),
        "order_latin_title": queryset_names(names_to_select["order"], "latin_title"),
        "family_title": queryset_names(names_to_select["family"], "title"),
        "family_latin_title": queryset_names(names_to_select["family"], "latin_title"),
        "genus_title": queryset_names(names_to_select["genus"], "title"),
        "genus_latin_title": queryset_names(names_to_select["genus"], "latin_title"),
    }


@register.simple_tag(name="separate_form")
def separate_slice(form, separating_index):
    form, separating_index = list(form), int(separating_index)
    return form[:separating_index], form[separating_index:]
