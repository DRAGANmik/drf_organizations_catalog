from rest_framework import serializers
from .models import Organization, Employee, Phone, PhoneType, Position
from django.shortcuts import get_object_or_404
from users.models import Support
from django.db.models import Q


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        organization = Organization.objects.create(**validated_data)
        Support.objects.create(
            user=request.user, organization=organization, creator=True
        )
        return organization


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"


class PhoneSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = "__all__"

    def to_representation(self, instance):
        return {"phone": "{}: {}".format(instance.phone_type, instance.number)}


class PhoneCreateSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True)
    phone_type = serializers.CharField(write_only=True)

    def validate(self, data):

        number = data["phone_number"]
        if number[0] != "+":
            raise serializers.ValidationError(
                "Некорректный формат номера. Ожидается код '+' "
            )
        if not number[1:].isnumeric():
            raise serializers.ValidationError(
                "Некорректный формат номера. Ожидаются цифры."
            )
        return data


class EmployeeSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

    def to_representation(self, instance):
        phone = PhoneSearchSerializer(instance.phone.all(), many=True)
        employee = {
            "id": instance.id,
            "employee": {
                "info": "{} {} {} ({})".format(
                    instance.last_name,
                    instance.first_name,
                    instance.patronymic,
                    instance.position.title,
                ),
                "contact": [phone.data],
            },
        }
        return employee


class EmployeeCreateUpdateSerializer(serializers.ModelSerializer):

    phone = PhoneCreateSerializer(many=True)

    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "patronymic", "position", "phone"]

    def validate(self, data):

        org_id = self.context.get("org_id")
        request = self.context.get("request")
        organization = get_object_or_404(Organization, id=org_id)

        employee = Employee.objects.filter(
            first_name=data["first_name"],
            last_name=data["last_name"],
            patronymic=data["patronymic"],
            organization=organization,
        )
        if employee:
            if request.method == "POST":
                raise serializers.ValidationError("Такой сотрудник уже есть!")
            elif (
                request.method == "PUT"
                or request.method == "PATCH"
                and employee
            ):
                pk = self.context.get("pk")
                for item in employee:
                    if int(pk) != item.pk:
                        raise serializers.ValidationError(
                            "Такой сотрудник уже есть!"
                        )
        return data

    def validate_phone(self, data):
        phone = data
        org_id = self.context.get("org_id")
        request = self.context.get("request")
        organization = get_object_or_404(Organization, id=org_id)
        employees_phone = Phone.objects.filter(
            employee__in=organization.employees.all()
        ).filter(phone_type__title="Личный")

        if phone:
            for item in phone:
                if item["phone_type"] == "Личный":
                    for el in employees_phone:
                        if el.number == item["phone_number"]:
                            if (
                                request.method == "PUT"
                                or request.method == "PATCH"
                            ):
                                pk = self.context.get("pk")
                                if not el.employee_set.filter(pk=pk):
                                    raise serializers.ValidationError(
                                        "Это личный номер другого сотрудника."
                                    )
        elif request.method == "POST":
            raise serializers.ValidationError(
                "Необходимо ввести номер телефона."
            )
        return data

    def create(self, validated_data):
        org_id = self.context.get("org_id")
        phone = validated_data.pop("phone")
        organization = get_object_or_404(Organization, id=org_id)
        employee = Employee.objects.create(
            **validated_data, organization=organization
        )
        for item in phone:
            phone_type, created = PhoneType.objects.get_or_create(
                title=item["phone_type"]
            )
            phone = Phone.objects.create(
                number=item["phone_number"], phone_type=phone_type
            )
            employee.phone.add(phone)
        return employee

    def update(self, instance, validated_data):
        phone = validated_data.pop("phone")
        if phone:
            instance_phone_list = [item for item in instance.phone.all()]
            for item in phone:

                phone_type, create = PhoneType.objects.get_or_create(
                    title=item["phone_type"]
                )
                phone = Phone.objects.create(
                    phone_type=phone_type, number=item["phone_number"]
                )
                if phone in instance_phone_list:
                    instance_phone_list.remove(phone)
                else:
                    instance.phone.add(phone)
            for item in instance_phone_list:
                item.delete()
        employee = Employee.objects.filter(id=instance.id)
        employee.update(**validated_data)
        return instance


class OrganizationReadSerializer(serializers.ModelSerializer):
    employees = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ["id", "name", "employees"]

    def get_employees(self, obj):
        request = self.context.get("request")
        search = request.query_params.get("search")
        return EmployeeSearchSerializer(
            obj.employees.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(patronymic__icontains=search)
                | Q(position__title__icontains=search)
                | Q(phone__number__icontains=search)
            ).distinct()[:5],
            many=True,
        ).data
