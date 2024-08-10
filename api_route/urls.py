from rest_framework import routers
from django.urls import path, include
from .views import RouteSerializerViewSet, OriginSerializerViewSet, DestinationSerializerViewSet, InstanceSerializerViewSet, UserSerializerViewSet, PerfilSerializerViewSet
router = routers.DefaultRouter()
router.register(r'api-route', RouteSerializerViewSet)

router.register(r'api-instance', InstanceSerializerViewSet)
router.register(r'api-origin', OriginSerializerViewSet)
router.register(r'api-destination', DestinationSerializerViewSet)
router.register(r'api-user', UserSerializerViewSet)
router.register(r'api-perfil', PerfilSerializerViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
