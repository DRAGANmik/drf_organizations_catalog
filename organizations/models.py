from django.db import models
from django.core.exceptions import ValidationError


class Organization(models.Model):
    address = models.CharField(max_length=100)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, related_name="employees"
    )
    position = models.ForeignKey(
        "Position", on_delete=models.SET_NULL, null=True
    )
    phone = models.ManyToManyField("Phone")

    def __str__(self):
        return "{} {} {}".format(
            self.first_name, self.last_name, self.patronymic
        )

    def clean(self):
        employee = Employee.objects.filter(
            first_name=self.first_name,
            last_name=self.last_name,
            patronymic=self.patronymic,
            organization=self.organization,
        )
        if self not in employee and employee:
            raise ValidationError("Такой сотрудник уже есть!")


class Position(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Phone(models.Model):
    phone_type = models.ForeignKey(
        "PhoneType", on_delete=models.SET_NULL, null=True
    )
    number = models.CharField(max_length=15)

    def __str__(self):
        return "{}: {}".format(self.phone_type.title, self.number)

    def clean(self):
        number = self.number

        if number[0] != "+":
            raise ValidationError(
                "Некорректный формат номера. Ожидается код '+'"
            )
        if not number[1:].isnumeric():
            raise ValidationError(
                "Некорректный формат номера. Ожидаются цифры."
            )


class PhoneType(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title
