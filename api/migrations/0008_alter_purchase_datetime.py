# Generated by Django 4.0.3 on 2022-03-22 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_product_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='datetime',
            field=models.DateTimeField(default='2006-10-25 14:30:59'),
        ),
    ]
