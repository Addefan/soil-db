import os

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from soil.celery import app
from web.models import Plant, Staff
from web.tasks_utils import prepare_queryset
from web.transitions import queryset_to_xlsx

# TODO celery task принимает только сериализуемые переменные (из них здесь только user_id, columns).
#  Видно, что эта функция в celery воркере никогда не запускалась.
@app.task
def export_to_excel(request, receiver, columns, user_id, qs=Plant.objects.prefetch_related("organization").all()):
    prepared_qs = prepare_queryset(columns, qs)
    path = queryset_to_xlsx(prepared_qs)
    user = Staff.objects.get(id=user_id)
    protocol = "https" if request.is_secure() else "http"
    context = {
        "origin": f"{protocol}://{request.get_host()}",
        "full_name": f"{user.name} {user.surname}",
        "path_to_file": os.path.basename(path),
    }
    html_content = render_to_string("emails/export_excel.html", context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject="Экспорт данных в excel", body=text_content, from_email=settings.DEFAULT_FROM_EMAIL, to=[receiver]
    )
    email.attach_alternative(html_content, "text/html")
    email.attach_file(path)
    email.send()
    # os.remove(path)


@app.task
def send_password_changing_email(request, user_id, token):
    user = Staff.objects.get(id=user_id)
    subject = "Смена пароля Soil DB"
    protocol = "https" if request.is_secure() else "http"
    html_context = {
        "subject": subject,
        "origin": f"{protocol}://{request.get_host()}",
        "full_name": f"{user.name} {user.surname}",
        "token": token,
    }
    html_message = render_to_string("emails/password_changing.html", html_context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message)
