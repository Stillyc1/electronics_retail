from rest_framework.routers import DefaultRouter

from electronics_retail.apps import ElectronicsRetailConfig
from electronics_retail.views import ElectronicsRetailViewSet

app_name = ElectronicsRetailConfig.name

router = DefaultRouter()
router.register(prefix=r"retail", viewset=ElectronicsRetailViewSet, basename='retails')

urlpatterns = [] + router.urls
