# Generated by Django 5.1.2 on 2024-10-24 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_caravan_resource_caravan_departure_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caravan',
            name='return_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
