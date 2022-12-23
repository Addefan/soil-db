import eav
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager as DjangoUserManager, PermissionsMixin
from django.db import models


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


class Plant(models.Model):
    number = models.IntegerField(unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    genus = models.ForeignKey(Genus, on_delete=models.SET_NULL, null=True)
    latin_name = models.CharField(max_length=127)
    name = models.CharField(max_length=127)


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
    name = models.CharField(max_length=127, verbose_name="Имя")
    surname = models.CharField(max_length=127, verbose_name="Фамилия")
    email = models.EmailField(unique=True, max_length=320, verbose_name="Почта")

    USERNAME_FIELD = "email"


eav.register(Plant)
