# Generated by Django 4.0.5 on 2022-07-03 20:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_rename_topbid_bids_top_bid_remove_bids_creator_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionproduct',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 3, 20, 20, 10, 458438)),
        ),
        migrations.AlterField(
            model_name='bids',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 3, 20, 20, 10, 458438)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 3, 20, 20, 10, 458438)),
        ),
        migrations.AlterUniqueTogether(
            name='wishlist',
            unique_together={('user', 'product')},
        ),
    ]