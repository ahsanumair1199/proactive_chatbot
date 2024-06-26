# Generated by Django 5.0 on 2023-12-18 10:41

import pgvector.django
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='addmessage',
            name='image_url',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='addmessage',
            name='video_url',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='embedding',
            field=pgvector.django.VectorField(blank=True, dimensions=3),
        ),
    ]
