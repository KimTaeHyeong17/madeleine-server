# Generated by Django 3.0.8 on 2020-07-19 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200715_1358'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('check_number', models.CharField(max_length=5)),
            ],
        ),
    ]
