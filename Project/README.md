# Description of the project 
It is an API for a website that displays a catalog of comics and books. This Api allows you to receive books and comics, read comics and books, rate them, leave comments. It also allows you to more quickly search for the works you need. For this, methods are used that search for several fields.


# Applications of the project
There are three apps: `auth`_, `base`, `core`.

`auth`_ application for authorization and registration of users. The main models are Custom User and Profile.
The `base` app is the basis for the `core` app. It contains the main models, such as: Publisher, Author, Category, Rating, Type, Genre and JournalBase. JournalBase is an abstract class for the Book and Comic models. `core` application contains models Book, Comic, Comment.


# Methods of the project
This API uses standard CRUD methods and additional specific methods such as `get_comics_by_category()`, `get_comics_by_genre()`, `get_books_by_genre()`, `get_comics_by_type()`

# Installed apps or Prerequisites
 REST Framework and REST Framework JWT
To install this, you need to write this commands in your terminal:

`pip install djangorestframework`

`pip install djangorestframework-jwt`
 
# Database
Postgress 
 In order to use postgress database you need to write this command in your terminal:

`pip install psycopg2`

# How project works
First, there are two types of users in the project: admin and guest. Their functionality is separated by the role field and permissions. The actions that users can take depend on the role and permissions. An ordinary user is a guest, he/she can read, view, rate works, leave comments, he/she can also view information about authors and publishers of works. The admin can do everything a guest can, plus actions like updating or changing works, uploading new works and deleting them.

# How to run a project
To run a project on your computer or laptop, you need to download the project from the repository. Then open it up in your work environment. Install and configure the `postgress` database. Install `rest framework` and `rest framework jwt`. Make `migrations` and `create a user admin`.