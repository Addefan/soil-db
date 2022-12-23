from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


class StaffAdmin(DjangoUserAdmin):
    ordering = ("-last_login",)
    list_display = ("id", "email", "name", "surname", "last_login", "organization_name")
    list_filter = ("last_login",)

    def organization_name(self, obj):
        return obj.organization.name

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "organization":
            formfield.label_from_instance = lambda obj: f'{obj.name}'
        return formfield

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональная информация", {"fields": ("name", "surname")}),
        (
            "Доступы",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Даты", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "organization"),
            },
        ),
    )
