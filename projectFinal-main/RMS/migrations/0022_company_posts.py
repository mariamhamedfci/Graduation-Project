# Generated by Django 4.2.5 on 2024-01-30 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RMS', '0021_job_achievements_job_education_job_other_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='posts',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
