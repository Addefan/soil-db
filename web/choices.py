from eav.models import Attribute, Value

from web.enums import TaxonLevel
from web.models import Plant, Taxon, Organization


def xlsx_columns_default_choices() -> list[tuple[str, str]]:
    translate = Plant._translate | Plant._taxa | {"organization": "Организация"}
    return [
        (field.name + "__name" if field.name == "organization" else field.name, translate[field.name])
        for field in Plant._meta.fields
        if translate.get(field.name)
    ]


def attributes_default_choices() -> list:
    organizations = Organization.objects.all()
    return [
        {
            "english_name": "organization",
            "russian_name": "Организация",
            "type": Attribute.TYPE_TEXT,
            "values": [{"name": organization.name} for organization in organizations],
        }
    ]


def xlsx_columns_custom_choices() -> list[tuple[str, str]]:
    return [(eav_field.name, eav_field.name) for eav_field in Attribute.objects.all()]


def attributes_custom_choices() -> list:
    table = Value.objects.all().select_related("attribute")
    custom_attributes = []
    attributes_distinct = []
    for field in table:
        if field.attribute.name not in attributes_distinct:
            attributes_distinct.append(field.attribute.name)
            filtered_table = table.filter(attribute__name=field.attribute.name)
            attr = f"value_{field.attribute.datatype}"
            attr_type = field.attribute.datatype
            if (attr_type == Attribute.TYPE_INT or attr_type == Attribute.TYPE_FLOAT) and len(filtered_table) >= 2:
                max_min_values = [int(getattr(f, attr)) for f in filtered_table]
                values = [{"name": min(max_min_values)}, {"name": max(max_min_values)}]
            else:
                values = [{"name": getattr(f, attr)} for f in filtered_table]

            custom_attributes.append(
                {
                    "english_name": field.attribute.slug,
                    "russian_name": field.attribute.name,
                    "type": attr_type,
                    "values": values,
                }
            )
    return custom_attributes


def xlsx_columns_taxon_choices() -> list[tuple[str, str]]:
    taxon_choices = []
    for choice in TaxonLevel.choices:
        for prefix, suffix in zip(("", "latin_"), ("", " (лат.)")):
            if choice[0] == "kingdom":
                continue
            taxon_choices.append((prefix + choice[0], choice[1] + suffix))
    return taxon_choices


def attribute_taxon_choices() -> list:
    taxon_attributes = []
    for choice in TaxonLevel.choices:
        if choice[0] == "kingdom":
            continue
        filtered_qs = Taxon.objects.filter(level=choice[0])
        taxon_attributes.append(
            {
                "english_name": choice[0],
                "russian_name": choice[1],
                "type": Attribute.TYPE_TEXT,
                "values": [{"name": field.title} for field in filtered_qs],
            }
        )
    return taxon_attributes


def xlsx_columns_choices() -> list[tuple[str, str]]:
    return (
        [choice for choice in xlsx_columns_default_choices() if choice[0] != "genus"]
        + xlsx_columns_taxon_choices()
        + xlsx_columns_custom_choices()
    )


def xlsx_columns_choices_dict() -> dict:
    return {key: val for key, val in xlsx_columns_choices()} | {"id": "id"}
