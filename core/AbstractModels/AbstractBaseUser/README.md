# Abstract Base User
A basic abstracted user meant to be expanded and used via inheritance.

### Model Contains:
- Django Auth's UserManager
- An id field automatically set up and is primary key
- Email field
- Auto generated created field
- A string method returning either the users name or username
