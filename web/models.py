import eav
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager as DjangoUserManager, PermissionsMixin
from django.db import models
from eav.models import Entity


class Organization(models.Model):
    name = models.CharField(max_length=127)
    address = models.CharField(max_length=255)


class BaseTaxon(models.Model):
    title = models.CharField(max_length=127, unique=True)
    latin_title = models.CharField(max_length=127, unique=True)

    class Meta:
        abstract = True


class Phylum(BaseTaxon):
    pass


class Class(BaseTaxon):
    phylum = models.ForeignKey(Phylum, on_delete=models.SET_NULL, null=True)


class Order(BaseTaxon):
    class_name = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)


class Family(BaseTaxon):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)


class Genus(BaseTaxon):
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True)


class PlantModelMixin:
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

    def _get_organization_name(self):
        if hasattr(self.organization, "name"):
            return self.organization.name
        return "Не указано"

    def _get_eav_fields(self):
        dct: dict = {}
        for attr in Entity(self).get_all_attributes():
            value = getattr(self.eav, attr.name, None)
            if value is not None:
                dct[attr.name] = value
        return dct

    def _get_plant_classification(self):
        dct: dict = {}
        plant = self
        for taxon in self._taxons:
            plant = getattr(plant, taxon)
            for attr in self._suffix:
                dct[self._taxons[taxon] + self._suffix[attr]] = getattr(plant, attr, "Не указано")
            if plant is None:
                break
        return dct


class Plant(models.Model, PlantModelMixin):
    number = models.IntegerField(unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    genus = models.ForeignKey(Genus, on_delete=models.SET_NULL, null=True)
    latin_name = models.CharField(max_length=127)
    name = models.CharField(max_length=127)

    def to_dict(self):
        obj: dict = {
            self._translate[key]: value or "Не указано"
            for key, value in self.__dict__.items()
            if not (key in self._stop_list or key.endswith("_id"))
        }
        obj |= self._get_plant_classification()
        obj["Организация"] = self._get_organization_name()
        obj |= self._get_eav_fields()
        return obj


class UserManager(DjangoUserManager):
    def _create_user(self, email, password, commit=True, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)


class Staff(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=127)
    surname = models.CharField(max_length=127)
    email = models.EmailField(unique=True, max_length=320)

    USERNAME_FIELD = "email"


eav.register(Plant)
