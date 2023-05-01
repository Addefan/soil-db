from datetime import timedelta

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password

from web.models import PasswordChange, Staff
from web.tasks import send_password_changing_email, delete_change_password_request


def create_password_change_request(new_password, user_id, origin):
    new_password = make_password(new_password)
    password_change = PasswordChange(password=new_password, user_id=user_id)
    password_change.save()
    token = password_change.id

    send_password_changing_email.delay(origin, user_id, token)
    delete_change_password_request.apply_async(eta=timedelta(hours=1), args=(token,))


def process_password_change_request(request):
    token = request.POST.get("token")
    if token is None:
        return False

    password_change = PasswordChange.objects.filter(pk=token).first
    user_id = request.user.id

    # checking whether the link has expired
    if password_change is None:
        return False

    # checking whether who tried to change the password and who clicked the link is the same user
    if password_change.user_id != user_id:
        return False

    user = Staff.objects.get(pk=user_id)
    user.password = password_change.password
    user.save()
    update_session_auth_hash(request, user)
    return True
