from django.urls import path, include
from rest_framework.routers import DefaultRouter

from play.viewsets import ClientViewSet

router = DefaultRouter()
router.register("", ClientViewSet)

urlpatterns = [
    path("clients/", include(router.urls)),
]