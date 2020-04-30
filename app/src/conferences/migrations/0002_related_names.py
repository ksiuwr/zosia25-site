# Generated by Django 2.2.10 on 2020-02-16 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zosia',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='conferences', to='conferences.Place'),
        ),
    ]
