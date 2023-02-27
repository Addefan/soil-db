from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import SelectDateWidget
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from eav.models import Entity, Attribute

from web.choices import xlsx_columns_choices
from web.enums import TaxonLevel
from web.models import Plant, Staff, Taxon


TYPES = [
    ("default", "Не выбрано"),
    ("integer", "Целое число"),
    ("float", "Число с плавающей точкой"),
    ("string", "Строка"),
    ("date", "Дата"),
]
INPUT_TYPES = {
    "int": forms.IntegerField,
    "text": forms.CharField,
    "float": forms.FloatField,
    "date": forms.DateField,
}


LEVEL = {
    0: "phylum",
    1: "class",
    2: "order",
    3: "family",
    4: "genus",
}


def modernization_dict(classification):
    counter, level_numb = 1, 0
    dct = {}
    for field, name in classification.items():
        if LEVEL[level_numb] not in dct and counter < 2:
            dct[LEVEL[level_numb]] = [name]
            counter += 1
        else:
            dct[LEVEL[level_numb]].append(name)
            counter = 1
            level_numb += 1
    return dct


def make_chain(classification):
    dct = modernization_dict(classification)
    parent = Taxon.objects.filter(level="kingdom").first()
    for level, names in dct.items():
        obj = Taxon.objects.filter(Q(level=f"{level}") & Q(title=names[0]) & Q(latin_title=names[1])).first()
        if not obj:
            parent = Taxon(parent=parent, level=level, title=names[0], latin_title=names[1])
            parent.save()
        else:
            obj.parent = parent
            obj.save()
            parent = obj
    return parent


class PlantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update({"class": "form-control", "placeholder": "smt"})

    class Meta:
        model = Plant
        fields = "__all__"
        exclude = ["genus"]
        labels = {
            "name": _("Наименование растения"),
            "latin_name": _("Латинское наименование растения"),
            "number": _("Уникальный номер"),
            "organization": _("Наименование организации"),
            "genus": _("Род (лат.)"),
        }
        error_messages = {
            "number": {
                "unique": _("Проверьте, пожалуйста, уникальность введенного вами номера"),
            },
        }

    def is_valid(self):
        return (
            super(PlantForm, self).is_valid()
            and self.initial["attr_form_view"].is_valid()
            and self.initial["form_classification"].is_valid()
        )

    def save(self, *args, **kwargs):
        plant = super().save(*args, **kwargs)
        attrs = self.initial["attr_form_view"].cleaned_data
        classification = self.initial["form_classification"].cleaned_data
        if attrs and classification:
            genus = Taxon.objects.filter(latin_title=classification["genus_latin_title"], level="Genus").first()
            if not genus:
                genus = make_chain(classification)
            plant.genus = genus
            obj = Entity(plant)
            for attribute in obj.get_all_attributes():
                plant.eav.__setattr__(attribute.slug, attrs.get(attribute.slug))
            plant.save()
            return plant
        else:
            raise Http404


class TaxonForm(forms.Form):
    suffixes = {"title": "", "latin_title": " (лат.)"}
    taxons = {"phylum": "Отдел", "class": "Класс", "order": "Порядок", "family": "Семейство", "genus": "Род"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update({"class": "form-control", "placeholder": "smt", "list": f"{attr}"})

    for taxon in taxons:
        for key, value in suffixes.items():
            locals()[taxon + "_" + key] = forms.CharField(label=taxons[taxon] + value)


class AttributeFormView(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.eav_attrs = Entity(Plant).get_all_attributes()
        for attr in self.eav_attrs:
            if attr.datatype == "date":
                self.fields[attr.slug] = INPUT_TYPES[attr.datatype](widget=SelectDateWidget())
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
            self.fields[attr].widget.attrs.update({"class": input_class})

    name_attr = forms.CharField(label="Название")
    type_attr = forms.ChoiceField(widget=forms.Select, choices=TYPES, label="Тип данных")


class AuthForm(forms.Form):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

        for _, field in self.fields.items():
            field.widget.attrs["placeholder"] = "placeholder"

    email = forms.EmailField(widget=forms.EmailInput(attrs={"autofocus": True, "class": "form-control"}))
    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "form-control"}),
    )
    remember_me = forms.BooleanField(
        label="Запомнить меня", widget=forms.CheckboxInput(attrs={"class": "form-check-input"}), required=False
    )

    error_messages = {
        "invalid_login": _("Удостоверьтесь, что вы правильно ввели почту и пароль"),
    }

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        remember_me = self.cleaned_data.get("remember_me")

        if self.is_valid():
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                if not remember_me:
                    settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                else:
                    settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False

        return self.cleaned_data

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"email": self.cleaned_data["email"]},
        )


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["email"].widget.attrs["readonly"] = ""
        self.fields["password"].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = "placeholder"

    def clean(self):
        cleaned_data = super().clean()
        raw_password = cleaned_data["password"]
        if raw_password:
            cleaned_data["password"] = make_password(raw_password)
        else:
            del cleaned_data["password"]
        return cleaned_data

    class Meta:
        model = Staff
        widgets = {"email": forms.EmailInput(), "password": forms.PasswordInput()}
        labels = {"password": "Новый пароль"}
        fields = ("surname", "name", "email", "password")
        readonly_fields = ("email",)


class XlsxColumnsForm(forms.Form):
    columns = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={"checked": True}),
        choices=xlsx_columns_choices(),
    )
