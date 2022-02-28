# Set up virtual environment

On terminal:

```
python -m venv env
source env/bin/activate # env/Scripts/activate on Windows
```

# Install packages

```
pip install django
pip install djangorestframework
pip install python-dotenv
```

# Install MySQL Client

You need to have Python installed (version 3.6+ should be OK)

You need to have mysqlclient installed on your system. For Mac and Linux, then instructions here should work:
https://github.com/PyMySQL/mysqlclient

For Windows, these instructions should work:
https://stackoverflow.com/a/51164104

# Create project and .env file

```
django-admin startproject mysite
cd mysite
touch.env
```

Inside of the .env, add the appropriate keys and values for connection method.

## Proxy connection
```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=<DATABASE_NAME>
```

## User/pass connection
```
DB_HOST=<ACCESS HOST URL>
DB_PORT=3306
DB_DATABASE=<DATABASE_NAME>
DB_USER=<USERNAME>
DB_PASSWORD=<PLAIN TEXT>
MYSQL_ATTR_SSL_CA=/etc/ssl/certs/ca-certificates.crt
```

# Bring in Vitess database backend

```
git clone https://github.com/vitessio/vitess
cp -r vitess/support/django/custom_db_backends .
rm -r vitess
```

The backend from Vitess will disable features not available on the database like foreign keys.

# Start store app

```
python manage.py startapp store
```

# Config

In manage.py:

```
...
from dotenv import load_dotenv

def main():
    load_dotenv()
    ...
```

In mysite/settings.py:

Import os at top of file

```
import os
from pathlib import Path
```

Add rest_framework and store to installed apps
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'store',
]
```

Go to DATABASES. Should be line 79 and update.

For proxy connection:

```
DATABASES = {
    'default': {
        'ENGINE': 'django_psdb_engine',
        'NAME': os.environ.get('DB_NAME'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT')
    }
}
```

For username and password:

```
DATABASES = {
    'default': {
        'ENGINE': 'django_psdb_engine',
        'NAME': os.environ.get('DB_NAME'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'USER': os.environ.get('DB_USER')
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'OPTIONS': {'ssl': {'ca': os.environ.get('MYSQL_ATTR_SSL_CA')}}
    }
}
```

# Migrate the predefined models

```
python manage.py migrate
```

If you can do that, then you know you can connect to the database.

# Create category and product models

In store/models.py:

```
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
```

Make migrations and migrate

```
python manage.py makemigrations
python manage.py migrate
```

Create empty migration so you can add initial data

```
python manage.py makemigrations --empty store
```

Open file that was just created. Should be store/migrations/0002_...

Modify to look like this:

```
from django.db import migrations

def load_data(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    Product = apps.get_model('store', 'Product')

    category_one = Category.objects.create(
        name='Category 1', description='This is category 1')
    
    category_two = Category.objects.create(
        name='Category 2', description='This is category 2')

    Product.objects.create(
        name='Product 1', description='This is product 1', 
        image='https://via.placeholder.com/300.png?text=Product1', 
        category=category_one)

    Product.objects.create(
        name='Product 2', description='This is product 2', 
        image='https://via.placeholder.com/300.png?text=Product2', 
        category=category_two)

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]

```

Load the data by running migrate.

```
python manage.py migrate
```

# Code to create API endpoint

In store directory, create a file called serializers.py

In that file:

```
from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category']
```

In store/views.py:

```
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer
    
class ListProducts(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
```

Create urls.py in the store directory. It should have this:

```
from django.urls import path
from store import views

urlpatterns = [
    path('products/', views.ListProducts.as_view()),
]
```

Update mysite/urls.py to import the include function and add a second item to urlpatterns

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls'))
]
```

Start the server

```
python manage.py runserver
```

View endpoint

GET localhost:8000/products/

Django REST framework will generate an HTML page when the client is a browser, and JSON the client is 
something like cURL, Postman, or an HTTP library.