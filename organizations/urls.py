from django.urls import path, include
from .views import OrganizationViewSet, EmployeeViewSet, PositionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r"organizations/(?P<org_id>\d+)/employees",
    EmployeeViewSet,
    basename="employees",
)
router.register("organizations", OrganizationViewSet, basename="organizations")
router.register("positions", PositionViewSet, basename="positions")


urlpatterns = [
    path("", include(router.urls)),
]
