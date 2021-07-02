# Basic User Model
A basic user that contains a django REST view and Django template views. Model only contains get_absolute_url property method and an attribute called URL_view_name containing the view get_absolute_url will reverse

## Abstract Base User
A basic abstracted user meant to be expanded and used via inheritance.

### Contains:
- Django Auth's UserManager
- An id field automatically set up and is primary key
- Email field
- Auto generated created field
- A string method returning either the users name or username
