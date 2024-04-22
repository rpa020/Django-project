# Generated by Django 4.0.3 on 2022-04-27 20:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie', '0002_alter_movieshow_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genres',
            name='genre',
            field=models.CharField(choices=[('Action', 'Action'), ('Comedy', 'Comedy'), ('Drama', 'Drama'), ('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('Mystery', 'Mystery'), ('Romance', 'Romance'), ('Thriller', 'Thriller')], max_length=20, null='True', unique=True),
        ),
        migrations.AlterField(
            model_name='movieshow',
            name='poster',
            field=models.ImageField(upload_to='posters/'),
        ),
        migrations.AlterField(
            model_name='movieshow',
            name='release_date',
            field=models.DateField(),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('headline', models.CharField(blank=True, max_length=100)),
                ('review_text', models.CharField(blank=True, max_length=2500)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.movieshow')),
            ],
        ),
    ]
