# Generated by Django 4.2.5 on 2024-02-01 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RMS', '0033_rename_describtion_education_degree_education_fromto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicant',
            name='workexperience',
        ),
        migrations.CreateModel(
            name='workexperience',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('companyworked', models.CharField(max_length=100, null=True)),
                ('jobworked', models.CharField(max_length=1000, null=True)),
                ('describtion', models.CharField(max_length=1000, null=True)),
                ('applicant', models.ManyToManyField(to='RMS.applicant')),
            ],
        ),
    ]
