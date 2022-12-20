from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from eav.fields import EavDatatypeField
from eav.forms import BaseDynamicEntityForm
from eav.models import Attribute, Entity

from web.models import Plant


class PlantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update({'class': 'form-control'})

    # todo словарь с присваиваемыми типами данных
    for i in Entity(Plant).get_all_attributes():
        locals()[i.name] = forms.CharField(required=False)

    class Meta:
        model = Plant
        exclude = ['organization', 'genus']
        # widgets = {
        #     'organization': forms.Select(),
        #     'genus': forms.Select()
        # }

    def save(self, *args, **kwargs):
        plant = super().save(*args, **kwargs)
        obj = Entity(plant)
        for i in obj.get_all_attributes():
            plant.eav.__setattr__(i.name, self.cleaned_data[i.name])
        plant.save()
        return plant
