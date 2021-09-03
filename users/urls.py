from django.urls import path, include
from .views import SupportViewSet, CreateUserAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("support", SupportViewSet, basename="support")


urlpatterns = [
    path("", include(router.urls)),
    path("register", CreateUserAPIView.as_view()),
    path("api-auth/", include("rest_framework.urls")),
]
