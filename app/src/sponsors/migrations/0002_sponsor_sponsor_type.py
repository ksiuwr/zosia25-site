# Generated by Django 3.2.16 on 2022-11-29 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='sponsor_type',
            field=models.CharField(choices=[('0', 'Bronze'), ('1', 'Silver'), ('2', 'Gold')], max_length=1, verbose_name='Type'),
            preserve_default=False,
        ),
    ]
