# Generated by Django 4.0.3 on 2022-03-22 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_purchase_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
