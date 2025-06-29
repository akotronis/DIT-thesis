# Generated by Django 4.2.17 on 2024-12-16 17:29

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('interactions', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='text',
            field=models.TextField(default='No text'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('polygon', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zones', to='auth.group')),
            ],
        ),
    ]
