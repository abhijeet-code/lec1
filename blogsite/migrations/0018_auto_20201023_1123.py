# Generated by Django 3.0.9 on 2020-10-23 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_delete_bid'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Watchlist',
            new_name='Achievelist',
        ),
        migrations.RenameModel(
            old_name='Alllisting',
            new_name='Allblogs',
        ),
    ]