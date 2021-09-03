from django.contrib import admin
from django.contrib.admin import register
from .models import Organization, Employee, Position, Phone, PhoneType
from .forms import EmployeeAdminForm


@register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeAdminForm
    pass


admin.site.register(Position)
admin.site.register(Phone)
admin.site.register(PhoneType)
