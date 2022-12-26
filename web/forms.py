from django import forms

from web.models import Staff


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
