# Generated by Django 5.1.2 on 2024-10-24 23:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_caravan_domestic_land_caravan_foreign_land'),
    ]

    operations = [
        migrations.AddField(
            model_name='caravan',
            name='foreign_cargo',
            field=models.JSONField(default='{}'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='caravan',
            name='domestic_land',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domestic_caravans', to='core.land'),
        ),
        migrations.AlterField(
            model_name='caravan',
            name='foreign_land',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foreign_caravans', to='core.land'),
        ),
        migrations.AlterField(
            model_name='caravan',
            name='return_time',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]