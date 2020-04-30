# Generated by Django 2.2.10 on 2020-03-15 20:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_alter_field_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='lock',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room', to='rooms.RoomLock'),
        ),
        migrations.AlterField(
            model_name='roomlock',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locks', to=settings.AUTH_USER_MODEL),
        ),
    ]
