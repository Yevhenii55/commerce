# Generated by Django 4.2.1 on 2023-06-03 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auction_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='is_winner',
            field=models.BooleanField(default=False),
        ),
    ]