from django.views.generic import DetailView
from eav.models import Entity

from web.models import Plant


class PlantMixin:
    _translate: dict[str, str] = {
        "latin_name": "Вид(лат.)",
        "name": "Вид",
        "number": "Идентификатор",
    }
    _taxons: dict[str, str] = {
        "genus": "Род",
        "family": "Семейство",
        "order": "Порядок",
        "class_name": "Класс",
        "phylum": "Тип",
    }
    _suffix: dict[str, str] = {
        "latin_title": "(лат.)",
        "title": "",
    }
    _stop_list: set = {"_state", "eav", "id"}

    @staticmethod
    def get_organization_name(instance: Plant):
        if hasattr(instance.organization, "name"):
            return instance.organization.name
        return "Не указано"

    @staticmethod
    def get_eav_fields(plant):
        dct: dict = {}
        for attr in Entity(plant).get_all_attributes():
            value = getattr(plant.eav, attr.name, None)
            if value:
                dct[attr.name] = value
        return dct

    def get_plant_classification(self, plant: Plant):
        dct: dict = {}
        for taxon in self._taxons:
            plant = getattr(plant, taxon)
            for attr in self._suffix:
                dct[self._taxons[taxon] + self._suffix[attr]] = getattr(plant, attr, "Не указано")
            if plant is None:
                break
        return dct


class PlantDetailView(DetailView, PlantMixin):
    template_name = "web/plant.html"
    context_object_name = "plant"
    slug_field = "number"
    slug_url_kwarg = "number"

    def get_queryset(self):
        return Plant.objects.all()

    def get_object(self, queryset=None):
        instance = super(PlantDetailView, self).get_object(queryset)
        obj: dict = {
            self._translate[key]: value or "Не указано"
            for key, value in instance.__dict__.items()
            if not (key in self._stop_list or key.endswith("_id"))
        } | {"latin_name": instance.latin_name, "name": instance.name}
        obj |= self.get_plant_classification(instance)
        obj["Организация"] = self.get_organization_name(instance)
        obj |= self.get_eav_fields(instance)
        return obj
