# Generated by Django 3.2.10 on 2024-02-02 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabla_general', '0002_jornadas_suma_j'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('j1', models.CharField(max_length=1000)),
                ('j2', models.CharField(max_length=1000)),
                ('j3', models.CharField(max_length=1000)),
                ('j4', models.CharField(max_length=1000)),
                ('j5', models.CharField(max_length=1000)),
                ('j6', models.CharField(max_length=1000)),
                ('j7', models.CharField(max_length=1000)),
                ('j8', models.CharField(max_length=1000)),
                ('j9', models.CharField(max_length=1000)),
                ('j10', models.CharField(max_length=1000)),
                ('j11', models.CharField(max_length=1000)),
                ('j12', models.CharField(max_length=1000)),
                ('j13', models.CharField(max_length=1000)),
                ('j14', models.CharField(max_length=1000)),
                ('j15', models.CharField(max_length=1000)),
                ('j16', models.CharField(max_length=1000)),
                ('j17', models.CharField(max_length=1000)),
            ],
        ),
    ]