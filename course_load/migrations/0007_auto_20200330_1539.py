# Generated by Django 3.0.4 on 2020-03-30 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_load', '0006_department_comment_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='comment_file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
