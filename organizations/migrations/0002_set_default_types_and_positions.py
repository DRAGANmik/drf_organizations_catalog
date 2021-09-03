from django.db import migrations


def set_default_types(apps, schema_editor):
    phone_types = ['Рабочий', 'Личный', 'Факс']
    PhoneType = apps.get_model("organizations", "PhoneType")
    for item in phone_types:
        PhoneType.objects.create(title=item)


def set_default_positions(apps, schema_editor):
    Position = apps.get_model("organizations", "Position")

    with open("data/positions.txt", "r") as f:
        for line in f.readlines():

            Position.objects.create(title=line.rstrip('\n'))


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_default_types),
        migrations.RunPython(set_default_positions),
    ]
