# Generated by Django 3.1 on 2020-08-26 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20200826_2233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Gender',
            new_name='gender',
        ),
    ]