# Generated by Django 2.1 on 2021-01-31 01:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_auto_20210130_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='catcher1',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='hello.Batter'),
        ),
    ]