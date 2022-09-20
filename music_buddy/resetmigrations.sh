#!/bin/bash

# Remove all migrations and load database with music data from the csv file

rm -f db.sqlite3 music_buddy_app/migrations/0*.py music_buddy_app/migrations/__pycache__/0*.pyc
rm -f db.sqlite3 account/migrations/0*.py account/migrations/__pycache__/0*.pyc
python manage.py makemigrations && python manage.py migrate
echo "*********************************************"
echo "Server has started"
python manage.py runserver

# Now load music data from the csv file into Django's database
