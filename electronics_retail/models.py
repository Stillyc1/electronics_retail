from django.db import models


class Product(models.Model):
    """Модель продукта, которую реализует сеть по продаже электроники"""
    name = models.CharField(max_length=128, verbose_name="название электроники")
    model = models.CharField(max_length=128, verbose_name="модель электроники")
    date_release = models.DateField(verbose_name="дата выхода продукта на рынок")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ElectronicsRetail(models.Model):
    """Модель объекта сети по продаже электроники"""
    LEVEL_NAME_RETAIL = ["Завод", "Розничная сеть", "Индивидуальный предприниматель"]

    _level_retail = models.PositiveIntegerField(verbose_name="Уровень иерархии сети", blank=True,
                                                null=True)
    level_name_retail = models.CharField(max_length=30, choices=[(x, x) for x in LEVEL_NAME_RETAIL],
                                         verbose_name="юридический статус сети")
    name = models.CharField(max_length=128, unique=True, verbose_name="название")
    email = models.EmailField(verbose_name="e-mail компании")
    country = models.CharField(max_length=100, verbose_name="страна")
    city = models.CharField(max_length=100, verbose_name="город")
    street = models.CharField(max_length=100, verbose_name="улица")
    house_number = models.CharField(max_length=10, verbose_name="номер дома")
    products = models.ManyToManyField(Product, related_name="electronics_retail")
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name="поставщик", blank=True,
                                 null=True, default=None)
    debt = models.DecimalField(max_digits=16, decimal_places=2, verbose_name="задолженность перед поставщиком",
                               default=0.00)
    date_time_born = models.DateTimeField(verbose_name="время создания", auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    @property
    def level_retail(self):
        return self._level_retail

    @level_retail.setter
    def level_retail(self, value):
        self._level_retail = value

    def save(self, *args, **kwargs):
        """Переопределяем метод, для указания уровня в иерархии сети"""
        if self.level_name_retail == "Завод":
            self.level_retail = 0

        if self.supplier:
            # Проверяем уровень поставщика
            if self.supplier.level_retail == 1:
                self.level_retail = 2
            elif self.supplier.level_retail == 0:
                self.level_retail = 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Сеть продажи электроники'
        verbose_name_plural = 'Сети продажи электроники'
