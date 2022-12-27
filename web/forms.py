from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from eav.models import Attribute, Entity
from web.models import Plant, Family, Order, Class, Phylum, Genus, Staff

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


class AttributeFormView(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr in Entity(Plant).get_all_attributes():
            self.fields[attr.name] = INPUT_TYPES[attr.datatype]
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update({"class": "form-control", "placeholder": "smt"})


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


class AttributeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update({"class": "form-control"})

    name_attr = forms.CharField(label="Название")
    type_attr = forms.ChoiceField(widget=forms.Select, choices=TYPES, label="Тип данных")


class GenusForm(forms.ModelForm):
    prefix = "genus"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "smt",
                    "list": f"character_{attr}_{self.prefix}",
                }
            )

    class Meta:
        model = Genus
        fields = ("title", "latin_title")
        # fields = '__all__'
        labels = {
            "title": _("Род"),
            "latin_title": _("Род (лат.)"),
        }


class FamilyForm(forms.ModelForm):
    prefix = "family"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "smt",
                    "list": f"character_{attr}_{self.prefix}",
                }
            )

    class Meta:
        model = Family
        fields = ("title", "latin_title")
        labels = {
            "title": _("Семейство"),
            "latin_title": _("Семейство (лат.)"),
        }


class OrderForm(forms.ModelForm):
    prefix = "order"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "smt",
                    "list": f"character_{attr}_{self.prefix}",
                }
            )

    class Meta:
        model = Order
        fields = ("title", "latin_title")
        labels = {
            "title": _("Порядок"),
            "latin_title": _("Порядок (лат.)"),
        }


class ClassForm(forms.ModelForm):
    prefix = "klass"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "smt",
                    "list": f"character_{attr}_{self.prefix}",
                }
            )

    class Meta:
        model = Class
        fields = ("title", "latin_title")
        labels = {
            "title": _("Класс"),
            "latin_title": _("Класс (лат.)"),
        }


class PhylumForm(forms.ModelForm):
    prefix = "phylum"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr, value in self.fields.items():
            self.fields[attr].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "smt",
                    "list": f"character_{attr}_{self.prefix}",
                }
            )

    class Meta:
        model = Phylum
        fields = ("title", "latin_title")
        labels = {
            "title": _("Отдел"),
            "latin_title": _("Отдел (лат.)"),
        }


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
