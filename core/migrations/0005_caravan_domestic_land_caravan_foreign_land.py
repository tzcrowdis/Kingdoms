# Generated by Django 5.1.2 on 2024-10-24 21:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_caravan_return_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='caravan',
            name='domestic_land',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='domestic_caravan', to='core.land'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='caravan',
            name='foreign_land',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='foreign_caravan', to='core.land'),
            preserve_default=False,
        ),
    ]
