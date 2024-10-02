# Timetablemaker
A simple website created with Python and the Django framework, inspired by my former boss who spent a good part of his workday creating tomorrows schedule based on the availability of me and my coworkers.

## CURRENTLY BROKEN, will fix

## How to use
I hope I've included all the neccessary files, apologies for any  istakes as this is my first commit, my job hunt has given me the final push to show some of my (finished-ish) projects.
The first step is to create a virtual environment on your machine and installing the requrements.txt libraries. The first step is to migrate, using `python3 manage.py migrate`, follwed by `python3 manage.py makemigrations`. Then, the second step would be to create a superuser with `python3 manage.py createsuperuser`. And with that, after running `python3 manage.py runserver`, you'll have access to the website and the admin dashboard, with the ability to create new users and timetables and so on with the web-based UI.

## Notes
this project is far from finished and there are redundant files littered around, one day I'll get around to sorting them and organising them better, and the algorithm is also somewhat rudimentary and need some adjusting for edge case scenarios, but it was my first full stack project and I'm pretty happy with how it turned out.
