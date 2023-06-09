# Generated by Django 4.2.1 on 2023-05-27 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MealManager', '0020_recipe_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutrients',
            name='carbs',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutrients',
            name='energyKcal',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutrients',
            name='energyKj',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutrients',
            name='fat',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutrients',
            name='fatSaturated',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutrients',
            name='protein',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutrients',
            name='salt',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutrients',
            name='sugar',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
