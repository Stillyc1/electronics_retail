from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображает модели сотрудников в админ-панели."""

    list_display = ("id", "username",)
    list_filter = ("username",)
    search_fields = ("id", "username",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.none()

    def save_model(self, request, obj, form, change):
        """Хэшируем пароль при создании сотрудника через админ-панель."""
        if form.cleaned_data['password']:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)
