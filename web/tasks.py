from django.db.models import QuerySet

from soil.celery import app
from web.models import Plant
from web.tasks_utils import prepare_queryset
from web.transitions import queryset_to_xlsx


@app.task
def export_to_excel(columns: list[str], qs: QuerySet = Plant.objects.prefetch_related("organization").all()):
    pseudo_queryset = prepare_queryset(columns, qs)
    path = queryset_to_xlsx(pseudo_queryset)
    print("path:", path)
    print("PSEUDO_QUERYSET:", pseudo_queryset)
