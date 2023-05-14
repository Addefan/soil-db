from django.utils.timezone import now

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
