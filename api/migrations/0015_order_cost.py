# Generated by Django 4.2.7 on 2023-11-22 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_order_bar_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cost',
            field=models.IntegerField(null=True),
        ),
    ]
