# Generated by Django 3.0.4 on 2020-04-06 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_load', '0011_course_comcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='comcode',
            field=models.IntegerField(),
        ),
    ]
