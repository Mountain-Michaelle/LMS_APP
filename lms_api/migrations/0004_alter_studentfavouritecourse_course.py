# Generated by Django 4.2.4 on 2024-06-05 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms_api', '0003_alter_course_teacher_alter_courserating_student_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentfavouritecourse',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms_api.coursechapter'),
        ),
    ]
