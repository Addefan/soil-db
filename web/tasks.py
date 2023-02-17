from django.core.mail import EmailMessage

from soil.celery import app
from web.models import Plant
from web.transitions import queryset_to_xlsx


@app.task
def export_to_excel(from_here, to_there):
    path = queryset_to_xlsx(Plant.objects.all())
    email = EmailMessage(
        subject="Файл xlsx", body="Вы успешно экспортировали таблицу!", from_email=from_here, to=[to_there]
    )
    email.attach_file(path)
    email.send()
