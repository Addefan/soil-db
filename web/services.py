import os
import django
from django.utils.timezone import now

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soil.settings")
django.setup()

from web.models import Plant


def create_plant_number() -> int:
    date = now().date()
    last_plant = Plant.objects.filter(digitized_at__gte=date).order_by("-digitized_at").first()

    if not last_plant:
        return int(f"{date.year % 100}{date.month:02}{date.day:02}1")

    serial_number = int(str(last_plant.number)[6:]) + 1
    number = int(f"{date.year % 100}{date.month:02}{date.day:02}{serial_number}")

    return number
