import eav
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager as DjangoUserManager, PermissionsMixin
from django.db import models
from eav.models import Entity
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from web.enums import TaxonLevel


class Organization(models.Model):
    name = models.CharField(max_length=127)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Taxon(MPTTModel):
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    level = models.CharField(choices=TaxonLevel.choices, max_length=7)
    title = models.CharField(max_length=127)
    latin_title = models.CharField(max_length=127)

    class MPTTMeta:
        level_attr = "mptt_level"
        order_insertion_by = ["title"]

    class Meta:
        unique_together = ("level", "title", "latin_title")

    def __str__(self):
        return self.title


class PlantModelMixin:
    _translate: dict[str, str] = {
        "latin_name": "Вид (лат.)",
        "name": "Вид",
        "number": "Идентификатор",
        "digitized_at": "Дата и время оцифровки",
    }
    _taxons: dict[str, str] = {
        "genus": "Род",
        "family": "Семейство",
        "order": "Порядок",
        "class": "Класс",
        "phylum": "Тип",
    }
    _suffix: dict[str, str] = {
        "latin_title": " (лат.)",
        "title": "",
    }
    _stop_list: set = {"_state", "eav", "id"}

    def _get_organization_name(self):
        if hasattr(self.organization, "name"):
            return self.organization
        return "Не указано"

    def _get_eav_fields(self):
        dct: dict = {}
        for attr in Entity(self).get_all_attributes():
            value = getattr(self.eav, attr.slug, None)
            if value is not None:
                dct[attr.name] = value
        return dct

    def _get_plant_classification(self):
        dct: dict = {}
        plant_taxon: Taxon = Taxon.objects.get(id=self.genus_id)
        plant_classification_tree = plant_taxon.get_ancestors(include_self=True, ascending=True)
        for taxon in plant_classification_tree:
            if taxon.level == "kingdom":
                continue
            for title in self._suffix:
                dct[self._taxons[taxon.level] + self._suffix[title]] = getattr(taxon, title, None)
        return dct


class Plant(models.Model, PlantModelMixin):
    number = models.IntegerField(unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    genus = models.ForeignKey(Taxon, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=127)
    latin_name = models.CharField(max_length=127)
    digitized_at = models.DateTimeField(auto_now_add=True)

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

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        organization = Organization.objects.get_or_create(name="Superuser Organization", address="")
        extra_fields.setdefault("organization_id", organization.id)
        return self._create_user(email, password, **extra_fields)


class Staff(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=127, verbose_name="Имя")
    surname = models.CharField(max_length=127, verbose_name="Фамилия")
    email = models.EmailField(unique=True, max_length=320, verbose_name="Почта")

    USERNAME_FIELD = "email"

    @property
    def is_staff(self):
        return self.is_superuser


eav.register(Plant)
