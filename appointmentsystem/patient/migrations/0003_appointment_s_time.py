# Generated by Django 4.2 on 2025-07-18 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='s_time',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
