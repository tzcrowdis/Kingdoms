# Generated by Django 5.1.2 on 2024-10-24 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caravan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource', models.CharField(choices=[(0, 'Metal'), (1, 'Food')], max_length=1)),
            ],
        ),
        migrations.AddField(
            model_name='scout',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='scoutknowledge',
            name='visit_time',
            field=models.DateTimeField(),
        ),
    ]