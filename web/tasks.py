import os

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from soil.celery import app
from web.models import Plant, Staff
from web.tasks_utils import prepare_queryset
from web.transitions import queryset_to_xlsx


@app.task
def export_to_excel(from_here, to_there, columns, user_id, qs=Plant.objects.prefetch_related("organization").all()):
    prepared_qs = prepare_queryset(columns, qs)
    path = queryset_to_xlsx(prepared_qs)
    user = Staff.objects.get(id=user_id)
    context = {
        "origin": "http://127.0.0.1:8000",
        "full_name": f"{user.name} {user.surname}",
        "path_to_file": os.path.basename(path),
    }
    html_content = render_to_string("emails/export_excel.html", context)
    text_contetn = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject="Экспорт данных в excel", body=text_contetn, from_email=from_here, to=[to_there]
    )
    email.attach_alternative(html_content, "text/html")
    # email.attach_file(path)
    email.send()
    # os.remove(path)


@app.task
def send_password_changing_email(user_id, token):
    user = Staff.objects.get(id=user_id)
    subject = "Смена пароля Soil DB"
    html_context = {
        "subject": subject,
        "origin": "http://127.0.0.1:8000",
        "full_name": f"{user.name} {user.surname}",
        "token": token,
    }
    html_message = render_to_string("emails/password_changing.html", html_context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message)
