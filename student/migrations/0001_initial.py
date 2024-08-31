# Generated by Django 5.0.7 on 2024-08-31 00:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.PositiveIntegerField(unique=True)),
                ('year_of_study', models.IntegerField()),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='accounts.userprofile')),
            ],
        ),
    ]
