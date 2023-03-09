from typing import Iterable

from django import forms
from django.db.models import Q
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from eav.models import Entity, Value

from web.models import Taxon, Plant
from web.services import create_plant_number

LEVEL = {
    0: "phylum",
    1: "class",
    2: "order",
    3: "family",
    4: "genus",
}


def modernization_dict(classification):
    counter, level_numb = 1, 0
    dct = {}
    for field, name in classification.items():
        if LEVEL[level_numb] not in dct and counter < 2:
            dct[LEVEL[level_numb]] = [name]
            counter += 1
        else:
            dct[LEVEL[level_numb]].append(name)
            counter = 1
            level_numb += 1
    return dct


def fill_out_taxon_parents(dct: dict, taxa: Iterable) -> None:
    """method fills out Taxon table 'parent_id' columns according to plant hierarchy"""
    created_taxa = {
        (taxon.level, taxon.title, taxon.latin_title): taxon.id for taxon in Taxon.objects.bulk_create(taxa)
    }
    keys = list(dct.keys())
    for key in range(len(keys) - 1):
        taxon = dct[keys[key]]
        taxon_id = taxon.id or created_taxa.get((taxon.level, taxon.title, taxon.latin_title))
        dct[keys[key + 1]].parent_id = taxon_id
    Taxon.objects.bulk_update(dct.values(), fields=["parent_id"])


def make_chain(classification):
    dct = modernization_dict(classification)
    taxa_dct = dict.fromkeys(dct)
    parent = Taxon.objects.filter(level="kingdom").first()
    created_taxa = []
    for level, names in dct.items():
        obj = Taxon.objects.filter(Q(level=f"{level}") & Q(title=names[0]) & Q(latin_title=names[1])).first()
        if not obj:
            parent = Taxon(parent_id=getattr(parent, "id", None), level=level, title=names[0], latin_title=names[1])
            created_taxa.append(parent)
        else:
            obj.parent_id = getattr(parent, "id", None)
            parent = obj
        taxa_dct[level] = parent
    fill_out_taxon_parents(taxa_dct, created_taxa)
    return parent


class PlantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update({"class": "form-control", "placeholder": "smt"})

    class Meta:
        model = Plant
        fields = "__all__"
        exclude = ["number", "genus", "digitized_at", "organization"]
        labels = {
            "name": _("Наименование растения"),
            "latin_name": _("Латинское наименование растения"),
            "number": _("Уникальный номер"),
            "organization": _("Организация"),
            "genus": _("Род (лат.)"),
        }
        error_messages = {
            "number": {
                "unique": _("Проверьте, пожалуйста, уникальность введенного вами номера"),
            },
        }

    def is_valid(self):
        return (
            super(PlantForm, self).is_valid()
            and self.initial["attr_form_view"].is_valid()
            and self.initial["form_classification"].is_valid()
        )

    @staticmethod
    def prepare_bulk_edit_eav_fields(plant: Plant, attrs: dict) -> tuple[list, list, set]:
        obj = Entity(plant)
        previous_values: dict = {
            val.attribute.slug: val for val in Value.objects.prefetch_related("attribute").filter(entity_id=plant.id)
        }
        created_values: list = []
        updated_values: list = []
        updated_fields: set = set()
        for attribute in obj.get_all_attributes():
            # if attribute wasn't filled out by user, skip it
            if attrs[attribute.slug] is None or attrs[attribute.slug] == "":
                continue
            # get current custom attribute value
            current_value = getattr(previous_values.get(attribute.slug), f"value_{attribute.datatype}", None)
            if current_value and current_value != attrs[attribute.slug]:
                # current value isn't equals to form attribute value => should update attribute value
                setattr(previous_values.get(attribute.slug), f"value_{attribute.datatype}", attrs[attribute.slug])
                updated_values.append(previous_values[attribute.slug])
                # bulk_update() method requires "fields" param
                updated_fields.add(f"value_{attribute.datatype}")
            # current value is None
            # it means that attribute value is filled out for the first time(need to create it)
            elif current_value is None:
                created_values.append(
                    Value(
                        **{f"value_{attribute.datatype}": attrs[attribute.slug]},
                        entity_id=plant.id,
                        attribute=attribute,
                        # redundant column
                        # if assign value 7 to entity_ct_id, it will work fine
                        entity_ct_id=7,
                    )
                )
        return created_values, updated_values, updated_fields

    def save(self, *args, **kwargs):
        self.instance.number = create_plant_number()
        self.instance.organization = self.initial["user_organization"]
        plant = super().save(*args, **kwargs)
        attrs = self.initial["attr_form_view"].cleaned_data
        classification = self.initial["form_classification"].cleaned_data
        if attrs and classification:
            genus = Taxon.objects.filter(latin_title=classification["genus_latin_title"], level="Genus").first()
            if not genus:
                genus = make_chain(classification)
            plant.genus = genus
            created_values, updated_values, updated_fields = self.prepare_bulk_edit_eav_fields(plant, attrs)
            if created_values:
                Value.objects.bulk_create(created_values)
            if updated_values:
                Value.objects.bulk_update(updated_values, fields=updated_fields)
            plant.save()
            return plant
        else:
            raise Http404


class TaxonForm(forms.Form):
    suffixes = {"title": "", "latin_title": " (лат.)"}
    taxa = {"phylum": "Отдел", "class": "Класс", "order": "Порядок", "family": "Семейство", "genus": "Род"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update({"class": "form-control", "placeholder": "smt", "list": f"{attr}"})

    for taxon in taxa:
        for key, value in suffixes.items():
            locals()[taxon + "_" + key] = forms.CharField(label=taxa[taxon] + value)
