from django.db import models
from django.contrib.auth import get_user_model
from organizations.models import Organization

User = get_user_model()

User._meta.get_field("email")._unique = True
User._meta.get_field("email").blank = False
User._meta.get_field("email").null = False


class Support(models.Model):
    """
    If support object is creator
    it can edit organization
    else can edit only employees in bind organization
    """

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    creator = models.BooleanField(default=False)
