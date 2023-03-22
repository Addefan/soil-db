from eav.models import Attribute, Value

from web.enums import TaxonLevel
from web.models import Plant


def xlsx_columns_default_choices() -> list[tuple[str, str]]:
    translate = Plant._translate | Plant._taxa | {"organization": "Организация"}
    return [
        (field.name + "__name" if field.name == "organization" else field.name, translate[field.name])
        for field in Plant._meta.fields
        if translate.get(field.name)
    ]


def attributes_default_choices() -> dict:
    plants = Plant.objects.all()
    return {
        "organization": [
            {f"{plant.organization}": Attribute.TYPE_TEXT}
            for plant in plants.filter(organization__isnull=False).distinct("organization")
        ],
        "genus": [
            {f"{plant.genus}": Attribute.TYPE_TEXT} for plant in plants.filter(genus__isnull=False).distinct("genus")
        ],
    }


def xlsx_columns_custom_choices() -> list[tuple[str, str]]:
    return [(eav_field.name, eav_field.name) for eav_field in Attribute.objects.all()]


def attributes_custom_choices() -> dict:
    table = Value.objects.all().select_related("attribute")
    custom_attributes = {}
    for field in table:
        if field.attribute.name not in custom_attributes.keys():
            filtered_table = table.filter(attribute__name=field.attribute.name)
            attr = f"value_{field.attribute.datatype}"
            custom_attributes[field.attribute.name] = [
                {f"{getattr(f, attr)}": f.attribute.datatype for f in filtered_table}
            ]
    return custom_attributes


def xlsx_columns_taxon_choices() -> list[tuple[str, str]]:
    taxon_choices = []
    for choice in TaxonLevel.choices:
        for prefix, suffix in zip(("", "latin_"), ("", " (лат.)")):
            if choice[0] == "kingdom":
                continue
            taxon_choices.append((prefix + choice[0], choice[1] + suffix))
    return taxon_choices


def xlsx_columns_choices() -> list[tuple[str, str]]:
    return (
        [choice for choice in xlsx_columns_default_choices() if choice[0] != "genus"]
        + xlsx_columns_taxon_choices()
        + xlsx_columns_custom_choices()
    )


def xlsx_columns_choices_dict() -> dict:
    return {key: val for key, val in xlsx_columns_choices()} | {"id": "id"}
