# Generated by Django 3.0.4 on 2020-03-23 00:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('l_count', models.IntegerField(default=0)),
                ('t_count', models.IntegerField(default=0)),
                ('p_count', models.IntegerField(default=0)),
                ('student_count', models.IntegerField(default=0)),
                ('max_strength', models.IntegerField(default=0)),
                ('course_type', models.CharField(choices=[('C', 'CDC'), ('E', 'Elective')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='course_load.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('psrn_or_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('instructor_type', models.CharField(choices=[('F', 'Faculty'), ('S', 'PHD Student')], max_length=1)),
                ('department', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='course_load.Department')),
            ],
        ),
        migrations.CreateModel(
            name='CourseInstructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_type', models.CharField(choices=[('L', 'Lecture'), ('T', 'Tutorial'), ('P', 'Practical'), ('I', 'Independent')], max_length=1)),
                ('course', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='course_load.Course')),
                ('instructor', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='course_load.Instructor')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='course_load.Department'),
        ),
        migrations.AddField(
            model_name='course',
            name='ic',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='course_load.Instructor'),
        ),
    ]
