from rest_framework.serializers import ModelSerializer

from electronics_retail.models import ElectronicsRetail, Product


class ProductSerializer(ModelSerializer):
    """Сериализатор для представления объекта сети."""

    class Meta:
        model = Product
        fields = "__all__"


class ElectronicsRetailSerializer(ModelSerializer):
    """Сериализатор для представления объекта сети."""
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = ElectronicsRetail
        fields = "__all__"
