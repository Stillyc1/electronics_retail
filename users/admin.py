from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображает модели сотрудников в админ-панели."""

    list_display = ("id", "username",)
    list_filter = ("username",)
    search_fields = ("id", "username",)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(form.cleaned_data["password"])
        obj.save()
