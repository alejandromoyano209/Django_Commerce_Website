# Generated by Django 3.1 on 2021-03-07 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_auctionlist_winneruser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlist',
            name='winneruser',
            field=models.CharField(max_length=64),
        ),
    ]