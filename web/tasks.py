from django.db.models import QuerySet

from soil.celery import app


def prepare_data(qs: QuerySet, columns: list[str]):
    # TODO execute queries to get necessary data
    ...


@app.task
def export_to_excel():
    pass
