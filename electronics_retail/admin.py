from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from electronics_retail.forms import ElectronicsRetailForm
from electronics_retail.models import Product, ElectronicsRetail


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Отображает модели продуктов в админ-панели."""

    list_display = ("id", "name", "model", "date_release",)
    list_filter = ("name", "model", "date_release",)
    search_fields = ("name", "model", "date_release",)


@admin.register(ElectronicsRetail)
class ElectronicsRetailAdmin(admin.ModelAdmin):
    """Отображает модели сети по продаже электроники в админ-панели."""

    list_display = ("_level_retail", "name", "supplier_link", "debt",)
    list_filter = ("city",)
    search_fields = ("id", "name", "supplier",)
    form = ElectronicsRetailForm
    actions = ['clear_debt']

    def supplier_link(self, obj):
        if obj.supplier:
            # Получаем URL для редактирования объекта supplier
            url = reverse('admin:electronics_retail_electronicsretail_change', args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"
    supplier_link.short_description = 'Поставщик'  # Название столбца в админке

    def clear_debt(self, request, queryset):
        queryset.update(debt=0.00)
        self.message_user(request, "Задолженность успешно очищена.")
    clear_debt.short_description = "Очистить задолженность перед поставщиком"
