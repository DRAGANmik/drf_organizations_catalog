from rest_framework import serializers
from .models import Support
from django.shortcuts import get_object_or_404

# from users.models import Support
from django.contrib.auth import get_user_model
from organizations.models import Organization
from organizations.serializers import OrganizationSerializer
from django.contrib.auth.password_validation import validate_password


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SupportCreateSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source="user.email")

    class Meta:
        model = Support
        fields = ["user"]

    def validate(self, data):
        user_email = data.get("user")
        org_id = self.context.get("organization")
        request = self.context.get("request")
        user = User.objects.filter(**user_email)
        if not user:
            raise serializers.ValidationError("Пользователь не найден.")
        support = Support.objects.filter(
            user=user.first(), organization_id=org_id
        )

        if support and request.method == "POST":
            raise serializers.ValidationError(
                "Данному пользователю уже предоставлен доступ."
            )
        elif not support and request.method == "DELETE":
            raise serializers.ValidationError(
                "Данного пользователя нет в списке поддержки."
            )
        return user_email

    def create(self, validated_data):
        user = User.objects.get(**validated_data)
        org_id = self.context.get("organization")
        organization = get_object_or_404(Organization, id=org_id)
        support = Support.objects.create(organization=organization, user=user)
        return support


class SupportSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = Support
        fields = ["id", "organization", "creator"]


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]

    def create(self, validated_data):
        """
        "username" field will duplicate email
        """
        user = User.objects.create(
            username=validated_data["email"],
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user
