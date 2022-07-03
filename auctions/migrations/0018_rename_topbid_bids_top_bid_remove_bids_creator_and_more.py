# Generated by Django 4.0.5 on 2022-07-03 19:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_alter_auctionproduct_time_alter_bids_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bids',
            old_name='topBid',
            new_name='top_bid',
        ),
        migrations.RemoveField(
            model_name='bids',
            name='creator',
        ),
        migrations.AddField(
            model_name='bids',
            name='bider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userBids', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auctionproduct',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 3, 19, 44, 41, 983499)),
        ),
        migrations.AlterField(
            model_name='bids',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productBids', to='auctions.auctionproduct'),
        ),
        migrations.AlterField(
            model_name='bids',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 3, 19, 44, 41, 984502)),
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.auctionproduct')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1000)),
                ('time', models.DateTimeField(default=datetime.datetime(2022, 7, 3, 19, 44, 41, 984502))),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userComment', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productComment', to='auctions.auctionproduct')),
            ],
        ),
    ]