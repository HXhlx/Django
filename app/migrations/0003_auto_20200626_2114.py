# Generated by Django 3.0.7 on 2020-06-26 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200626_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_date',
            field=models.DateTimeField(null=True),
        ),
    ]
