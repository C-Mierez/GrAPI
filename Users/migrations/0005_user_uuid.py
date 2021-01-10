# Generated by Django 3.1.5 on 2021-01-10 05:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_user_deleted_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
