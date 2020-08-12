# Changes Log

Make the clients following to the project changes

## Live Demo

you can check out a live demo [of it here!](https://h-changeslog-5qt8mm16v6.herokuapp.com/) hosted on [heroku](https://heroku.com)

> *username*: err
>
> *password*: 12345

## Getting Started

### Prerequisites

- [Python3.6](https://www.python.org/downloads/) or later

### Installing

#### Create virtual environment

``` bash
pip install --upgrade virtualenv
virtualenv -p python3 env
source env/bin/activate && cd env
```

#### Clone The repository, install dependencies and run

``` bash
(env) $ git clone https://mohamed17717@bitbucket.org/mohamed17717/changes-log.git src && cd src
(env) $ pip install -r requirements.txt
(env) $ python manage.py makemigrations
(env) $ python manage.py migrate
(env) $ python manage.py createsuperuser
(env) $ python manage.py runserver
```

## Built With

- **Django** -  The web framework used

## Features

### There is 2 types of accounts

1. **User**
      1. can't see other users or others projects
      2. see only his projects
      3. make comment on changes
      4. edit the comment
2. **Admin**
      1. List of all users and projects in homepage
      2. create new user
      3. search in users and projects
      4. create project
      5. ( create | update | edit ) versions
      6. ( create | update | edit ) changes
      7. replay for user comment
