from datetime import timedelta, datetime

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password

from web.models import PasswordChange, Staff
from web.services.url import build_origin_from_request
from web.tasks import send_password_changing_email, delete_change_password_request


def create_password_change_request(request):
    new_password = request.POST.get("password")
    user_id = request.user.id
    origin = build_origin_from_request(request)

    new_password = make_password(new_password)
    password_change = PasswordChange.objects.create(password=new_password, user_id=user_id)
    token = password_change.id

    send_password_changing_email.delay(origin, user_id, token)
    delete_change_password_request.apply_async((token,), eta=datetime.now() + timedelta(seconds=30))


def process_password_change_request(request):
    token = request.GET.get("token")
    if token is None:
        return False

    password_change = PasswordChange.objects.filter(pk=token).first()
    user_id = request.user.id

    # checking whether the link has expired
    if password_change is None:
        return False

    user = Staff.objects.get(pk=user_id)
    user.password = password_change.password
    user.save()
    update_session_auth_hash(request, user)
    return True
