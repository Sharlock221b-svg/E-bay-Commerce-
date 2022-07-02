# Generated by Django 4.0.5 on 2022-07-02 13:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionproduct',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='auctionproduct',
            name='category',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='auctionproduct',
            name='image_url',
            field=models.URLField(blank=True, max_length=500),
        ),
    ]
