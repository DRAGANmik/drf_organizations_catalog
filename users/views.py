from .serializers import (
    SupportSerializer,
    CreateUserSerializer,
)

from .models import Support

from rest_framework.mixins import ListModelMixin

from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import GenericViewSet

from rest_framework import permissions


class ListViewSet(ListModelMixin, GenericViewSet):
    pass


class CreateUserAPIView(CreateAPIView):
    """
    Register user
    """

    serializer_class = CreateUserSerializer


class SupportViewSet(ListViewSet):
    """
    Show for request.user organizations which can be edit
    """

    serializer_class = SupportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Support.objects.filter(user=self.request.user).order_by(
            "-creator"
        )
