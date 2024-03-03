# Project Overview
### LogIn Page
![LogIn Page](https://github.com/SuhelKhanCA/lushlyrics-webapp-django/assets/112371384/be85b904-e404-45ed-af29-eb52fd7d9bbe)
### Sign Up Page
![SignUp Page)](https://github.com/SuhelKhanCA/lushlyrics-webapp-django/assets/112371384/0d7107ee-0a3b-41c9-9b10-b307dbfe23f4)

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/mohammedwed/Lushlyrics-insecure.git
$ cd lushlyrics-webapp-django
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd Lushlyrics-insecure
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.
