# Generated by Django 4.0.1 on 2022-03-21 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('movie', '0001_initial'),
	]

	operations = [
		migrations.AlterField(
			model_name='movieshow',
			name='genre',
			field=models.ManyToManyField(blank=True, to='movie.Genres'),
		),
	]
