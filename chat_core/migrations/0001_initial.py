# Generated by Django 5.1.4 on 2025-02-26 20:33

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=250)),
                ('file', models.FileField(upload_to='files/')),
                ('filename', models.CharField(max_length=500)),
                ('vectordb_path', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=500)),
                ('response_generated', models.CharField(max_length=1000)),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat_core.bots')),
            ],
        ),
    ]
