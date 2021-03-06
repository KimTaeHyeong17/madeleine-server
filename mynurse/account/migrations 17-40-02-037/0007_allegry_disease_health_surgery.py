# Generated by Django 3.0.8 on 2020-07-22 08:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20200721_0708'),
    ]

    operations = [
        migrations.CreateModel(
            name='Health',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregnant', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Surgery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surgery_name', models.TextField(max_length=50)),
                ('date', models.DateTimeField(auto_now=True)),
                ('health', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Health')),
            ],
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease_name', models.TextField(max_length=20)),
                ('health', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Health')),
            ],
        ),
        migrations.CreateModel(
            name='Allegry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allgergy_name', models.TextField(max_length=20)),
                ('health', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Health')),
            ],
        ),
    ]
