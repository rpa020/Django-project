# Generated by Django 4.0.1 on 2022-03-21 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

	initial = True

	dependencies = [
	]

	operations = [
		migrations.CreateModel(
			name='Genres',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('genre', models.CharField(choices=[('Action', 'Action'), ('Comedy', 'Comedy'), ('Drama', 'Drama'), ('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('Mystery', 'Mystery'), ('Romance', 'Romance'), ('Thriller', 'Thriller')], max_length=20, null='True')),
			],
		),
		migrations.CreateModel(
			name='MovieShow',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('title', models.CharField(max_length=50)),
				('release_date', models.IntegerField()),
				('poster', models.CharField(blank=True, max_length=1000)),
				('description', models.CharField(max_length=1000)),
				('category', models.CharField(choices=[('Movie', 'Movie'), ('Show', 'Show/Series')], max_length=50, null=True)),
				('genre', models.ManyToManyField(to='movie.Genres')),
			],
		),
	]