from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from eav.models import Entity
from web.models import Plant, Staff, Taxon

TYPES = [
    ("default", "Не выбрано"),
    ("integer", "Целое число"),
    ("float", "Число с плавающей точкой"),
    ("string", "Строка"),
    ("date", "Дата"),
]
INPUT_TYPES = {
    "int": forms.IntegerField(),
    "text": forms.CharField(),
    "date": forms.DateField(widget=forms.SelectDateWidget),
    "float": forms.FloatField(),
}


def make_array_from_dict(dct):
    array = []
    variable = []
    for k, v in dct.items():
        if len(variable) == 2:
            array.append(variable.copy())
            variable.clear()
            variable.append((k, v))
        else:
            variable.append((k, v))
    if len(variable) == 2:
        array.append(variable.copy())
    return array


def make_chain(classification):
    arr = make_array_from_dict(classification)
    print(classification["genus_title"])
    parent = Taxon.objects.filter(level__icontains="kingdom").first()
    print(arr)
    for level in arr:
        level_name = level[0][0].split("_")[0]
        title = level[0][1]
        latin_title = level[1][1]
        obj = (
            Taxon.objects.filter(level__icontains=f"{level_name}")
            .filter(Q(title=title) & Q(latin_title=latin_title))
            .first()
        )
        if not obj:
            parent = Taxon(parent=parent, level=level_name, title=title, latin_title=latin_title)
            parent.save()
        else:
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
                plant.eav.__setattr__(attribute.slug, attrs[attribute.name])
            plant.save()
            return plant
        else:
            raise Http404


class TaxonForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update({"class": "form-control", "placeholder": "smt", "list": f"{attr}"})

    phylum_title = forms.CharField(label="Отдел")
    phylum_latin_title = forms.CharField(label="Отдел (лат.)")
    class_title = forms.CharField(label="Класс")
    class_latin_title = forms.CharField(label="Класс (лат.)")
    order_title = forms.CharField(label="Порядок")
    order_latin_title = forms.CharField(label="Порядок (лат.)")
    family_title = forms.CharField(label="Семейство")
    family_latin_title = forms.CharField(label="Семейство (лат.)")
    genus_title = forms.CharField(label="Род")
    genus_latin_title = forms.CharField(label="Род (лат.)")


class AttributeFormView(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr in Entity(Plant).get_all_attributes():
            self.fields[attr.name] = INPUT_TYPES[attr.datatype]
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update({"class": "form-control", "placeholder": "smt"})


class AttributeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update({"class": "form-control"})

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
        self.fields["email"].widget.attrs["disabled"] = ""
        self.fields["password"].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = "placeholder"

    class Meta:
        model = Staff
        widgets = {"email": forms.EmailInput(), "password": forms.PasswordInput()}
        labels = {"password": "Новый пароль"}
        fields = ("surname", "name", "email", "password")
        readonly_fields = ("email",)
