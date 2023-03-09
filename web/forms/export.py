from django import forms

from web.choices import xlsx_columns_choices


class XlsxColumnsForm(forms.Form):
    columns = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={"checked": True}),
        choices=xlsx_columns_choices(),
    )
