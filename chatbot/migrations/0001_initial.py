# Generated by Django 5.0 on 2023-12-18 08:04

import django.db.models.deletion
import pgvector.django
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('message', models.TextField()),
                ('is_sent', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('sender', models.CharField(max_length=50)),
                ('receiver', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('image_url', models.CharField(blank=True, max_length=255)),
                ('video_url', models.CharField(blank=True, max_length=255)),
                ('level', models.CharField(blank=True, max_length=30)),
                ('embedding', pgvector.django.VectorField(dimensions=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('whatsapp_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.whatsappuser')),
            ],
        ),
        migrations.CreateModel(
            name='GptResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('text', models.TextField()),
                ('embedding', pgvector.django.VectorField(dimensions=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('whatsapp_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.whatsappuser')),
            ],
        ),
    ]
