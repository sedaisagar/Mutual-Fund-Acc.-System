# A minimal Django-based backend system to manage mutual funds and user investments, focusing on key API functionality

## Project Setup

### Clone the repository


### Create Virtual Environment
```
python -m venv venv 
```
### Activate Virtual Environment

#### Windows User
```
venv/Scripts/activate
```
#### Unix User
```
source venv/bin/activate
```

### Install Packages
```
pip install -r requirements
```

### Generate New Secret Key 
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### copy .env.sample file to .env
```
cp .env.sample .env
```
- Open .env file and set the key generated in earlier step in SECRET_KEY
- Set allowed hosts as many host as you want to allow or simple write * for ALLOWED_HOSTS to allow all origins or write hosts with comma separated hostnames like ```127.0.0.1,localhost,example.com```
- Set DEBUG value as ```True``` / ```False``` 

### Create Admin User
```python manage.py createsuperuser``` 

### Now Setup Is Complete
Running the django server

```python manage.py runserver```

### Swagger docs api endpoint
```
http://127.0.0.1:8000/api/doc/#/
```


# Project Overview

In this project I've assigned user with two roles namely 'A' For Admin and 'U' For User

Admin only creates and updates mutual fund (s), User and admin both are allowed to list mutual fund (s) create,list  investment(s) and list report(s). 



### Test For User Model
```
python manage.py test tests.models.user
```
### Test For Mutual Fund Model
```
python manage.py test tests.models.mutual_funds
```
### Test For User Investment Model
```
python manage.py test tests.models.investment
```
### Test For User Register Api
```
python manage.py test tests.apis.user_register
```
### Test For User Token Api(s)
```
python manage.py test tests.apis.token_obtain
```
### Test For Mutual Fund Api(s)
```
python manage.py test tests.apis.mutual_funds
```
### Test For Investments Api(s)
```
python manage.py test tests.apis.investments
```



