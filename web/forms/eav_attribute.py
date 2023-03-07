from django import forms
from eav.models import Entity

from web.enums import EavAttributeType
from web.models import Plant

INPUT_TYPES = {
    "int": forms.IntegerField,
    "text": forms.CharField,
    "float": forms.FloatField,
    "date": forms.DateField,
}


class AttributeMainForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.eav_attrs = Entity(Plant).get_all_attributes()
        for attr in self.eav_attrs:
            if attr.datatype == "date":
                self.fields[attr.slug] = INPUT_TYPES[attr.datatype](widget=forms.NumberInput(attrs={"type": "date"}))
            else:
                self.fields[attr.slug] = INPUT_TYPES[attr.datatype]()
            self.fields[attr.slug].required = False
            self.fields[attr.slug].label = attr.name
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update({"class": "form-control", "placeholder": "smt"})


class AttributeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr, value in self.fields.items():
            input_class = "form-select" if self.fields[attr].widget.input_type == "select" else "form-control"
            self.fields[attr].widget.attrs.update({"class": input_class, "placeholder": "smt"})

    name_attr = forms.CharField(label="Название")
    type_attr = forms.ChoiceField(widget=forms.Select, choices=EavAttributeType.choices, label="Тип данных")
