# Generated by Django 4.2.13 on 2024-10-02 03:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_factionknowledge_known'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factionknowledge',
            name='knower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='knowns', to='core.faction'),
        ),
        migrations.AlterField(
            model_name='factionknowledge',
            name='known',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='knowers', to='core.faction'),
        ),
    ]
