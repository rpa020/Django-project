# Generated by Django 4.0.3 on 2022-05-03 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_alter_genres_genre_alter_movieshow_poster_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movieshow',
            old_name='genre',
            new_name='genres',
        ),
        migrations.AlterField(
            model_name='genres',
            name='genre',
            field=models.CharField(choices=[('action', 'Action'), ('comedy', 'Comedy'), ('drama', 'Drama'), ('fantasy', 'Fantasy'), ('horror', 'Horror'), ('mystery', 'Mystery'), ('romance', 'Romance'), ('thriller', 'Thriller')], max_length=20, null='True', unique=True),
        ),
        migrations.AlterField(
            model_name='movieshow',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
