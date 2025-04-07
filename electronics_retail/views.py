from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from electronics_retail.models import ElectronicsRetail
from electronics_retail.permissions import IsActive
from electronics_retail.serializers import ElectronicsRetailSerializer


class ElectronicsRetailViewSet(ModelViewSet):
    """Реализация представления объекта сети через ViewSet (полный crud)"""
    serializer_class = ElectronicsRetailSerializer
    queryset = ElectronicsRetail.objects.all()
    permission_classes = (IsAuthenticated, IsActive,)
    filter_backends = [SearchFilter]
    search_fields = ['country']

    def perform_update(self, serializer):
        debt = self.request.data.get("debt")
        if debt or debt == 0:
            raise ValidationError("Нельзя изменять поле 'debt'!")
        super().perform_update(serializer)
