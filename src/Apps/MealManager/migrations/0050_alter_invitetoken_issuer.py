# Generated by Django 4.2.1 on 2023-06-23 17:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MealManager', '0049_alter_ingredientgroup_related_recipe_invitetoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitetoken',
            name='issuer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]