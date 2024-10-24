# Generated by Django 5.1.2 on 2024-10-24 20:41

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_caravan_scout_active_alter_scoutknowledge_visit_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caravan',
            name='resource',
        ),
        migrations.AddField(
            model_name='caravan',
            name='departure_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='caravan',
            name='domestic_cargo',
            field=models.JSONField(default='{}'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='caravan',
            name='return_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='land',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lands', to='core.faction'),
        ),
    ]
