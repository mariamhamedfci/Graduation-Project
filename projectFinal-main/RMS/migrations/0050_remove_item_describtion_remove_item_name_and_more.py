# Generated by Django 4.2.5 on 2024-02-06 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RMS', '0049_remove_applicant_sections_othersection_applicant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='describtion',
        ),
        migrations.RemoveField(
            model_name='item',
            name='name',
        ),
        migrations.RemoveField(
            model_name='item',
            name='section',
        ),
        migrations.AddField(
            model_name='othersection',
            name='describtion',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
