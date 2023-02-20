from functools import cached_property

from django.db.models import QuerySet, Q
from eav.models import Value

from web.choices import xlsx_columns_choices_dict, xlsx_columns_default_choices
from web.models import Taxon


class QuerySetToListConverter:
    def __init__(self, columns: list[str], qs: QuerySet):
        self.columns = set(columns)
        self.qs = qs
        self.translation = xlsx_columns_choices_dict()

    @cached_property
    def default_columns(self):
        default_columns = [
            choice[0] for choice in xlsx_columns_default_choices() if choice[0] in self.columns or choice[0] == "genus"
        ]
        return [
            {self.translation[key]: val for key, val in instance.items()}
            for instance in self.qs.values("id", *default_columns).order_by("id")
        ]

    @cached_property
    def taxon_columns(self):
        taxon_columns_queryset = {instance.id: instance for instance in Taxon.objects.all()}
        self.xlsx_taxon_columns = {}
        for obj in taxon_columns_queryset.values():
            if obj.level == "genus":
                leaf = obj.id
                self.xlsx_taxon_columns[leaf] = {}
                while obj:
                    for prefix in ("", "latin_"):
                        if prefix + obj.level in self.columns:
                            self.xlsx_taxon_columns[leaf][self.translation[prefix + obj.level]] = getattr(
                                obj, prefix + "title"
                            )
                    obj = taxon_columns_queryset.get(obj.parent_id)
        return self.xlsx_taxon_columns

    @cached_property
    def custom_columns(self):
        return [
            {self.translation[model.attribute.name]: model.value, "id": model.entity_id}
            for model in Value.objects.prefetch_related("attribute")
            .filter(Q(entity_id__in=[instance["id"] for instance in self.default_columns]))
            .order_by("id")
            if model.attribute.name in self.columns
        ]

    def get_all_columns(self):
        prepared_pseudo_queryset = self.default_columns
        # combine plant's default and taxon columns
        for obj in prepared_pseudo_queryset:
            genus = obj.pop("Род")
            obj |= self.taxon_columns[genus]
        custom_columns_pseudo_queryset = self.custom_columns
        # Two pointers method
        # combine plant's default and custom columns
        i, j = 0, 0
        while i < len(prepared_pseudo_queryset) and j < len(custom_columns_pseudo_queryset):
            if prepared_pseudo_queryset[i]["id"] == custom_columns_pseudo_queryset[j]["id"]:
                prepared_pseudo_queryset[i] |= custom_columns_pseudo_queryset[j]
                j += 1
            else:
                i += 1
        # All pseudo queryset dicts must have the same structure
        # so the missing fields must be present in each dict
        for instance in prepared_pseudo_queryset:
            instance.pop("id")
            instance |= {
                key: None for key in {self.translation[column] for column in self.columns}.difference(instance.keys())
            }
        return prepared_pseudo_queryset


def prepare_queryset(columns: list[str], qs) -> list[dict]:
    """qs - queryset with filters"""
    handler = QuerySetToListConverter(columns, qs)
    return handler.get_all_columns()
