# Generated by Django 2.2.4 on 2019-08-27 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190827_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='b_date',
            field=models.DateField(verbose_name='Birth Date'),
        ),
    ]