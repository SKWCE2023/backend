# Generated by Django 4.2.7 on 2023-11-22 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_order_order_completion_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='bar_code',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
