# Generated by Django 2.2.7 on 2019-11-23 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Join',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('region', models.CharField(max_length=200, null=True)),
                ('joined_people', models.IntegerField(default=0)),
                ('current_joined', models.BooleanField(default=True, max_length=200)),
                ('active_period', models.CharField(default=0, max_length=200)),
                ('purpose', models.CharField(max_length=200, null=True)),
                ('body', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('writer', models.CharField(max_length=200, null=True)),
                ('body', models.CharField(max_length=200, null=True)),
                ('picture', models.CharField(max_length=200, null=True)),
                ('score', models.IntegerField(default=0)),
            ],
        ),
    ]