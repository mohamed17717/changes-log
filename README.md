# Changes Log

Make the clients following to the project changes

## Live Demo

you can check out a live demo [of it here!](https://h-changeslog-5qt8mm16v6.herokuapp.com/) hosted on [heroku](https://heroku.com)

## Getting Started

### Prerequisites

- [Python3](https://www.python.org/downloads/).6 or later

### Installing

Create virtual environment

``` bash
$ pip install --upgrade virtualenv
$ virtualenv -p python3 env
$ source env/bin/activate && cd env
```

Clone The repository, install dependencies and run.

``` bash
(env) $ git clone https://github.com/mohamed17717/changes-log src && cd src
(env) $ pip install -r requirements.txt
(env) $ python manage.py makemigrations
(env) $ python manage.py migrate
(env) $ python manage.py runserver
```

## Built With

- Django -  The web framework used

## Features

There is 2 types of accounts

1. User
      - cant see other users or others projects
      - see only his projects
      - make comment on changes
      - edit the comment
1. Admin
      - List of all users and projects in homepage
      - create new user
      - search in users and projects
      - create project
      - ( create | update | edit ) versions
      - ( create | update | edit ) changes
      - replay for user comment
