# Generated by Django 3.1 on 2021-03-09 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0023_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlist',
            name='img',
            field=models.URLField(default=None),
        ),
    ]
