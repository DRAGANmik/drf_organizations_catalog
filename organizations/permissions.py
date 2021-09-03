from rest_framework.permissions import SAFE_METHODS, BasePermission
from users.models import Support
from .models import Organization
from django.shortcuts import get_object_or_404


class IsCreator(BasePermission):
    """
    Have access only creator.
    """

    def has_permission(self, request, view):
        organization = get_object_or_404(Organization, **view.kwargs)
        if request.user.id:
            creator = Support.objects.filter(
                user=request.user, organization=organization, creator=True
            )
            return request.user and creator
        return False


class IsCreatorOrReadOnly(BasePermission):
    """
    Have access only creator,
    or the request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif view.kwargs:
            organization = get_object_or_404(Organization, **view.kwargs)
            creator = Support.objects.filter(
                user=request.user, organization=organization, creator=True
            )
            return request.user and creator
        else:
            return request.user and request.user.is_authenticated


class IsSupport(BasePermission):
    """
    Allows access to support's users, or is a read-only request.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        organization = get_object_or_404(
            Organization, id=view.kwargs["org_id"]
        )
        creator = Support.objects.filter(
            user=request.user, organization=organization
        )
        return request.user and creator
