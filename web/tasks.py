from django.db.models import QuerySet, Q
from eav.models import Value

from soil.celery import app
from web.models import Plant, Taxon
from web.forms import plant_columns_default_choices


def prepare_data(columns: set[str], qs: QuerySet = Plant.objects.all()):
    # TODO execute queries to get necessary data
    default_columns = {choice[0] for choice in plant_columns_default_choices()} & set(columns)
    default_columns_pseudo_queryset = qs.prefetch_related("Taxon").values("id", *default_columns).order_by("id")
    taxon_columns_queryset = Taxon.objects.all()
    custom_columns_pseudo_queryset = [
        {model.attribute.name: model.value, "id": model.entity_id}
        for model in Value.objects.prefetch_related("attribute")
        .filter(Q(entity_id__in=[instance["id"] for instance in default_columns_pseudo_queryset]))
        .order_by("id")
    ]
    print(default_columns_pseudo_queryset, custom_columns_pseudo_queryset)


@app.task
def export_to_excel():
    pass
