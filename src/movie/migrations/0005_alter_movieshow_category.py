# Generated by Django 4.0.4 on 2022-05-08 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_rename_genre_movieshow_genres_alter_genres_genre_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movieshow',
            name='category',
            field=models.CharField(choices=[('Movie', 'Movie'), ('Show', 'Show')], max_length=50, null=True),
        ),
    ]
