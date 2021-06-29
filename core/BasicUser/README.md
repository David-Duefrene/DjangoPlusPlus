# Basic User
A basic user that currently contains only a django REST view inside of [API.py](API.py). Model only contains get_absolute_url property method and an attribute called URL_view_name containing the view get_absolute_url will reverse

## Abstract Base User
A basic abstracted user meant to be expanded and used via inheritance.

### Model Contains:
- Django Auth's UserManager
- An id field automatically set up and is primary key
- Email field
- Auto generated created field
- A string method returning either the users name or username
