# Generated by Django 3.0 on 2021-02-10 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=1)),
                ('age', models.SmallIntegerField()),
                ('image', models.FilePathField()),
            ],
        ),
    ]
