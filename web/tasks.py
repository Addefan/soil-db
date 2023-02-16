from django.db.models import QuerySet, Q
from eav.models import Value

from soil.celery import app
from web.models import Plant, Taxon
from web.tasks_utils import QuerySetToXlsxHandler


def prepare_data(columns: list[str], qs: QuerySet = Plant.objects.prefetch_related("organization").all()):
    print(columns)
    handler = QuerySetToXlsxHandler(set(columns), qs)
    print(handler.get_all_columns())
    # translation = xlsx_columns_choices_dict()
    # print(translation)
    # default_columns = {choice[0] for choice in xlsx_columns_default_choices()} & set(columns)
    # default_columns_pseudo_queryset = [
    #     {translation[key]: val for key, val in instance.items()}
    #     for instance in qs.values("id", *default_columns).order_by("id")
    # ]
    # taxon_columns_queryset = {instance.id: instance for instance in Taxon.objects.all()}
    # taxon_columns_pseudo_queryset = {}
    # for obj in taxon_columns_queryset.values():
    #     if obj.level == "genus":
    #         leaf = obj.id
    #         taxon_columns_pseudo_queryset[leaf] = {}
    #         while obj:
    #             for prefix in ("", "latin_"):
    #                 if prefix + obj.level in columns:
    #                     taxon_columns_pseudo_queryset[leaf][translation[prefix + obj.level]] = getattr(
    #                         obj, prefix + "title"
    #                     )
    #             obj = taxon_columns_queryset.get(obj.parent_id)
    # print(taxon_columns_queryset)
    # print(taxon_columns_pseudo_queryset)
    # for obj in default_columns_pseudo_queryset:
    #     genus = obj.pop("Род")
    #     obj |= taxon_columns_pseudo_queryset[genus]
    # custom_columns_pseudo_queryset = [
    #     {translation[model.attribute.name]: model.value, "id": model.entity_id}
    #     for model in Value.objects.prefetch_related("attribute")
    #     .filter(Q(entity_id__in=[instance["id"] for instance in default_columns_pseudo_queryset]))
    #     .order_by("id")
    #     if model.attribute.name in columns
    # ]
    # prepared_pseudo_queryset = default_columns_pseudo_queryset
    # i, j = 0, 0
    # while i < len(prepared_pseudo_queryset) and j < len(custom_columns_pseudo_queryset):
    #     if prepared_pseudo_queryset[i]["id"] == custom_columns_pseudo_queryset[j]["id"]:
    #         prepared_pseudo_queryset[i] |= custom_columns_pseudo_queryset[j]
    #         j += 1
    #     elif prepared_pseudo_queryset[i]["id"] < custom_columns_pseudo_queryset[j]["id"]:
    #         fill_dict = {}
    #         for key in custom_columns_pseudo_queryset[j]:
    #             # O(1) - custom_columns_pseudo_queryset object has fixed length("id" and custom field)
    #             if key != "id":
    #                 fill_dict[key] = None
    #         prepared_pseudo_queryset[i] |= fill_dict
    #         i += 1
    # print(prepared_pseudo_queryset, custom_columns_pseudo_queryset)


@app.task
def export_to_excel():
    pass
