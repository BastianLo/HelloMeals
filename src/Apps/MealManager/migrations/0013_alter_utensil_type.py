# Generated by Django 4.2.1 on 2023-05-23 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MealManager', '0012_ingredient_hellofreshimageurl_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utensil',
            name='type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]