# Generated by Django 4.0.3 on 2022-03-29 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_payment_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
