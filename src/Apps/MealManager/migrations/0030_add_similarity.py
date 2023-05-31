from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MealManager', '0029_alter_tagmerge_target'),
    ]

    operations = [
        TrigramExtension(),
    ]
