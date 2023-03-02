import os
import django
from django.utils.timezone import now

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soil.settings")
django.setup()

from web.models import Plant


def create_plant_number() -> int:
    date = now().date()
    last_plant = Plant.objects.filter(digitized_at__gte=date).order_by("-digitized_at").first()
    number = date.strftime("%y%m%d")

    if not last_plant:
        return int(f"{number}1")

    serial_number = int(str(last_plant.number)[6:]) + 1
    number = int(f"{number}{serial_number}")

    return number


if __name__ == "__main__":
    print(create_plant_number())
