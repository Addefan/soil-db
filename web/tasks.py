import os
from pathlib import Path

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from api.serializers import PlantSerializer
from soil.celery import app
from web.models import Plant, Staff, PasswordChange
from web.services import queryset_to_xlsx


@app.task
def export_to_excel(origin, columns, user_id, filters=None):
    # TODO: apply filters
    qs = Plant.objects.optimize_queries()
    prepared_qs = PlantSerializer(qs, context={"columns": columns}, many=True).data
    path = queryset_to_xlsx(prepared_qs)
    user = Staff.objects.get(id=user_id)
    context = {
        "origin": origin,
        "full_name": f"{user.name} {user.surname}",
        "path_to_file": os.path.basename(path),
    }
    html_content = render_to_string("emails/export_excel.html", context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject="Экспорт данных в excel", body=text_content, from_email=settings.DEFAULT_FROM_EMAIL, to=[user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.attach_file(path)
    email.send()
    default_storage.delete(Path(*path.parts[1:]))


@app.task
def send_password_changing_email(origin, user_id, token):
    user = Staff.objects.get(id=user_id)
    subject = "Смена пароля Soil DB"
    html_context = {
        "subject": subject,
        "origin": origin,
        "full_name": f"{user.name} {user.surname}",
        "token": token,
    }
    html_message = render_to_string("emails/password_changing.html", html_context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message)


@app.task
def delete_change_password_request(token):
    password_change = PasswordChange.objects.filter(pk=token).first()
    if password_change is not None:
        password_change.delete()
