# Generated by Django 5.0 on 2023-12-18 10:43

import pgvector.django
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0002_addmessage_image_url_addmessage_video_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='embedding',
            field=pgvector.django.VectorField(blank=True, dimensions=3, null=True),
        ),
    ]