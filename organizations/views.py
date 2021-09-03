from .serializers import (
    OrganizationSerializer,
    EmployeeCreateUpdateSerializer,
    OrganizationReadSerializer,
    EmployeeSearchSerializer,
    PositionSerializer
)
from rest_framework.viewsets import ModelViewSet
from .models import Organization, Position
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from users.serializers import SupportCreateSerializer, SupportSerializer
from users.models import Support
from .permissions import IsCreator, IsSupport, IsCreatorOrReadOnly
from rest_framework import filters
from users.views import ListViewSet


class PositionViewSet(ListViewSet):
    """
    List with available positions
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsCreatorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
        "employees__first_name",
        "employees__last_name",
        "employees__patronymic",
        "employees__position__title",
        "employees__phone__number",
    ]

    def get_serializer_class(self):
        if self.request.query_params.get("search"):
            return OrganizationReadSerializer

        if self.action == "add_del_support":
            return SupportCreateSerializer

        return OrganizationSerializer

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_path="add-del-support",
        url_name="add-delete-support",
        permission_classes=[IsCreator],
    )
    def add_del_support(self, request, pk):
        """
        Endpoint which add and delete users for edit employees info.
        For "DELETE" method need to put email in request
        Only for creator.
        """
        serializer = SupportCreateSerializer(
            data=request.data, context={"organization": pk, "request": request}
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "POST":

            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        support = Support.objects.filter(
            user__email=serializer.validated_data["email"], organization_id=pk
        )
        support.delete()
        return Response(
            {"deleted": serializer.validated_data["email"]},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        detail=True,
        methods=["GET"],
        url_path="supports",
        url_name="supports",
        permission_classes=[IsCreator],
    )
    def view_supports(self, request, pk):
        """
        List of users which can edit.
        Only for creator.
        """
        support = Support.objects.filter(organization_id=pk)
        serializer = SupportSerializer(support, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class EmployeeViewSet(ModelViewSet):
    permission_classes = [IsSupport]

    def get_serializer_class(self):
        if self.action != "list" and self.action != "retrieve":
            return EmployeeCreateUpdateSerializer
        return EmployeeSearchSerializer

    def get_serializer_context(self):
        return {**self.kwargs, "request": self.request}

    def get_queryset(self):
        org_id = self.kwargs["org_id"]
        organization = Organization.objects.get(pk=org_id)
        return organization.employees.all()

