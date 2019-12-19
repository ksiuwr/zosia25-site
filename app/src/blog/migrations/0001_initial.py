# Generated by Django 2.2.8 on 2019-12-13 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('publication', models.DateTimeField(auto_now_add=True, verbose_name='Publication date')),
            ],
            options={
                'ordering': ['-publication'],
                'get_latest_by': 'publication',
            },
        ),
    ]
