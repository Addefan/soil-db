from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from eav.fields import EavDatatypeField
from eav.forms import BaseDynamicEntityForm
from eav.models import Attribute, Entity
from django.utils.translation import gettext_lazy as _

from web.models import Plant, Family, Order, Class, Phylum

TYPES = [
    ("default", "Не выбрано"),
    ("integer", "Целое число"),
    ("float", "Десятичное число"),
    ("string", "Строка"),
    ("date", "Дата"),
]


class AttributeFormView(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in Entity(Plant).get_all_attributes():
            if i.datatype == "int":
                self.fields[i.name] = forms.IntegerField()
            elif i.datatype == "text":
                self.fields[i.name] = forms.CharField()
            elif i.datatype == "date":
                self.fields[i.name] = forms.DateField(widget=forms.SelectDateWidget)
            elif i.datatype == "float":
                self.fields[i.name] = forms.FloatField()
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update({"class": "form-control", "id": "floatingInput", "placeholder": "smt"})


class PlantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update({"class": "form-control", "id": "floatingInput", "placeholder": "smt"})

    class Meta:
        model = Plant
        fields = "__all__"
        labels = {
            "name": _("Наименование растения"),
            "latin_name": _("Латинское наименование растения"),
            "number": _("Уникальный номер"),
        }

    # def save(self, *args, **kwargs):
    #     print(*kwargs)
    #     plant = super().save(*args, **kwargs)
    #     obj = Entity(plant)
    #     for i in obj.get_all_attributes():
    #         plant.eav.__setattr__(i.name, self.cleaned_data[i.name])
    #     plant.save()
    #     return plant


class AttributeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update({"class": "form-control"})

    name_attr = forms.CharField(label="Название")
    type_attr = forms.ChoiceField(widget=forms.Select, choices=TYPES, label="Тип данных")


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = "__all__"


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = "__all__"


class PhylumForm(forms.ModelForm):
    class Meta:
        model = Phylum
        fields = "__all__"
