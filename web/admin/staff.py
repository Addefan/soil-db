from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


class StaffAdmin(DjangoUserAdmin):
    ordering = ("-last_login",)
    list_display = ("id", "email", "name", "surname", "last_login", "organization")
    list_filter = ("last_login",)

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
