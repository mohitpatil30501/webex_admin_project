# Generated by Django 3.1.7 on 2021-03-26 07:03

import Dashboard.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfilePicFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bytes', models.TextField()),
                ('filename', models.CharField(max_length=255)),
                ('mimetype', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('841f67ec-c045-4acb-9b24-cdfdcd504bb4'), primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('website', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, default=None, max_length=12, null=True)),
                ('mobile', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('address', models.CharField(blank=True, default=None, max_length=500, null=True)),
                ('date_of_birth', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('profile_file', models.FileField(blank=True, default=None, null=True, upload_to=Dashboard.models.profile_pic_file_name)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('e22c2ab0-ee4f-4482-adae-4125285398aa'), primary_key=True, serialize=False, unique=True)),
                ('designation', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('department', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('institute', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.teacher')),
            ],
        ),
    ]
