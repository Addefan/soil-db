from django.core.mail import EmailMessage

from soil.celery import app
from web.tasks_utils import prepare_queryset
from web.transitions import queryset_to_xlsx


@app.task
def export_to_excel(from_here, to_there, columns, qs):
    path = queryset_to_xlsx(prepare_queryset(columns, qs))
    email = EmailMessage(
        subject="Файл xlsx", body="Вы успешно экспортировали таблицу!", from_email=from_here, to=[to_there]
    )
    email.attach_file(path)
    email.send()
