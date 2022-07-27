# Learn how to integrate PlanetScale with a sample Django application

This sample application demonstrates how to connect to a PlanetScale MySQL database, create and run migrations, seed the database, and display the data.

For the full tutorial, see the [Django PlanetScale documentation](https://docs.planetscale.com/tutorials/connect-django-app).

## Set up the Django app

1. Clone the starter Django application:

```bash
git clone git@github.com:planetscale/django-example.git
cd django-example
```

2. Start the virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

For Windows, use `env/Scripts/activate`.

3. Install the required packages:

```bash
pip install -r ./requirements.txt
```

## Set up the database

1. Sign up for a [free PlanetScale account](https://planetscale.com/sign-up) and create a new database.

2. Click the "**Connect**" button to generate credentials for database branch (`main` is default). Select "**Django**" from the language dropdown and copy the values in the sample `.env` file.

3. Modify your `.env` file in your Django app with the values from the previous step:

```
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
MYSQL_ATTR_SSL_CA=
```

> **Note**: The value for `MYSQL_ATTR_SSL_CA` may differ [depending on your operating system](https://docs.planetscale.com/reference/secure-connections#ca-root-configuration).

4. In the `mysite/settings.py` file, scroll down and look for the `DATABASES` object. Replace it with the following:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_psdb_engine',
        'NAME': os.environ.get('DB_NAME'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'OPTIONS': {'ssl': {'ca': os.environ.get('MYSQL_ATTR_SSL_CA')}}
    }
}
```

## Run migrations and seeder

1. Change directory and run the migrations and seeder with:

```bash
cd mysite/
python manage.py migrate
```

## Start the application

1. Start the server with:

```bash
python manage.py runserver
```

2. Navigate to [`localhost:8000/products`](http://localhost:8000/products) to see a list of data from the products table. 
