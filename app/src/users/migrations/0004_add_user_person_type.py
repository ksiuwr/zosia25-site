# Generated by Django 3.2.16 on 2022-11-27 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_related_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFilters',
            fields=[
            ],
            options={
                'verbose_name_plural': 'User filters',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
        ),
        migrations.AlterModelOptions(
            name='userpreferences',
            options={'verbose_name_plural': 'User preferences'},
        ),
        migrations.AddField(
            model_name='user',
            name='person_type',
            field=models.CharField(choices=[('Sponsor', 'Sponsor'), ('Guest', 'Guest'), ('Normal', 'Normal')], default='Normal', max_length=16, verbose_name='Person type'),
        ),
    ]
