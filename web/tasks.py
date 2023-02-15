from django.db.models import QuerySet, Q
from eav.models import Value
from mptt.querysets import TreeQuerySet
from mptt.utils import drilldown_tree_for_node

from soil.celery import app
from web.models import Plant, Taxon
from web.forms import plant_columns_default_choices


def prepare_data(columns: list[str], qs: QuerySet = Plant.objects.all()):
    # TODO execute queries to get necessary data
    default_columns = {choice[0] for choice in plant_columns_default_choices()} & set(columns)
    default_columns_pseudo_queryset = qs.prefetch_related("Taxon").values("id", *default_columns).order_by("id")
    taxon_columns_queryset = {instance.id: instance for instance in Taxon.objects.all()}
    taxon_columns_pseudo_queryset = {}
    for obj in taxon_columns_queryset.values():
        if obj.level == "genus":
            leaf = obj.id
            taxon_columns_pseudo_queryset[leaf] = {}
            while obj and obj.parent_id:
                for prefix in ("", "latin_"):
                    if prefix + obj.level in columns:
                        taxon_columns_pseudo_queryset[leaf][prefix + obj.level] = getattr(obj, prefix + "title")
                obj = taxon_columns_queryset.get(obj.parent_id)
    print(taxon_columns_queryset)
    print(taxon_columns_pseudo_queryset)
    for obj in default_columns_pseudo_queryset:
        genus = obj.pop("genus")
        obj |= taxon_columns_pseudo_queryset[genus]
    custom_columns_pseudo_queryset = [
        {model.attribute.name: model.value, "id": model.entity_id}
        for model in Value.objects.prefetch_related("attribute")
        .filter(Q(entity_id__in=[instance["id"] for instance in default_columns_pseudo_queryset]))
        .order_by("id")
        if model.attribute.name in columns
    ]
    print(default_columns_pseudo_queryset, custom_columns_pseudo_queryset)


@app.task
def export_to_excel():
    pass
