# Generated by Django 3.0.5 on 2020-04-15 18:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('balance', models.PositiveIntegerField()),
                ('hold', models.PositiveIntegerField()),
                ('status', models.BooleanField(choices=[(True, 'Opened'), (False, 'Closed')], default=True)),
            ],
        ),
    ]
