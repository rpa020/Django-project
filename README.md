# Best Group

Film review web app

This project requires
- python 3.10^
- pillow 9.1.0~

And has only been tested with
- django 4.0.3^

To generate and populate the database: 
```
python3.10 manage.py migrate

python3.10 manage.py loaddata genres.json
```

And of course to run the app:
```
python3.10 manage.py runserver
```

To install the database:
1. Open documentation, and got to documentation/database/src
2. Copy db.sqlite3 from documentation/database/src into the folder of this Readme file (src/)
3. Migrate if neccessary
4. The database should be installed
