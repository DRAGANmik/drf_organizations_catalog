from django import forms
from django.core.exceptions import ValidationError
from .models import Phone


class EmployeeAdminForm(forms.ModelForm):
    def clean(self):
        employees_phone = Phone.objects.filter(
            employee__in=self.cleaned_data["organization"]
            .employees.all()
            .exclude(id=self.instance.id)
        ).filter(phone_type__title="Личный")
        phone = self.cleaned_data["phone"]

        if employees_phone:
            for item in phone:
                if item.phone_type.title == "Личный":
                    if item in employees_phone:
                        raise ValidationError(
                            "Это личный номер другого сотрудника."
                        )
