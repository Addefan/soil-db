from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager as DjangoUserManager, PermissionsMixin
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=127)
    address = models.CharField(max_length=255)


class BasePlantSystem(models.Model):
    title = models.CharField(max_length=127)

    class Meta:
        abstract = True


class Phylum(BasePlantSystem):
    pass


class Class(BasePlantSystem):
    phylum = models.ForeignKey(Phylum, on_delete=models.SET_NULL, on_update=models.CASCADE, null=True)


class Order(BasePlantSystem):
    class_name = models.ForeignKey(Class, on_delete=models.SET_NULL, on_update=models.CASCADE, null=True)


class Family(BasePlantSystem):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, on_update=models.CASCADE, null=True)


class Genius(BasePlantSystem):
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, on_update=models.CASCADE, null=True)


class Plant(models.Model):
    number = models.IntegerField()
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, on_update=models.CASCADE, null=True)
    genius = models.ForeignKey(Genius, on_delete=models.SET_NULL, null=True)
    latin_name = models.CharField(max_length=127)
    name = models.CharField(max_length=127)


class Property(models.Model):
    name = models.CharField(max_length=127)


class PlantsProperties(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, on_update=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, on_update=models.CASCADE)
    value = models.TextField()

    class Meta:
        unique_together = (('plant', 'property'),)


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


class Staff(models.Model, AbstractBaseUser, PermissionsMixin):
    object = UserManager()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, on_update=models.CASCADE)
    name = models.CharField(max_length=127)
    surname = models.CharField(max_length=127)
    email = models.EmailField(unique=True, max_length=320)

    @property
    def is_staff(self):
        return True

    USERNAME_FIELD = "email"
