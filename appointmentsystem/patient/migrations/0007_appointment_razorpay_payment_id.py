# Generated by Django 4.2 on 2025-07-20 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0006_appointment_cancellation_reason_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
