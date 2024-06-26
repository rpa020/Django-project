# Generated by Django 4.0.4 on 2022-05-20 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie', '0006_movieshow_director_movieshow_runtime_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movieshow',
            old_name='target_audience',
            new_name='age_rating',
        ),
        migrations.AddField(
            model_name='movieshow',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='movieshow',
            name='description',
            field=models.TextField(max_length=100000),
        ),
        migrations.AlterField(
            model_name='movieshow',
            name='director',
            field=models.CharField(default='Unknow', max_length=50),
        ),
        migrations.AlterField(
            model_name='movieshow',
            name='runtime',
            field=models.DurationField(default=0),
        ),
    ]
