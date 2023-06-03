# Generated by Django 4.2.1 on 2023-06-01 17:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auction_current_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='bids',
            field=models.ManyToManyField(related_name='auctions', through='auctions.Bid', to=settings.AUTH_USER_MODEL),
        ),
    ]
