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
python manage.py test tests.models.investments
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
## Api EndPoints

#### POST - /api/register/

```
Example Payload:
{
  "email": "user@example.com",
  "password": "string"
}

Example Success Response:
{
  "message": "Operation Success",
  "data": {
    "id": "ef09c3d5-2ca0-4773-842e-a7f2316f0631",
    "email": "user@example.com"
  }
}, 
Example Error Response:
{
  "message": "Validation Error",
  "data": {
    "type": "validation_error",
    "errors": [
      {
        "code": "unique",
        "detail": "user with this Email Address already exists.",
        "attr": "email"
      }
    ]
  }
}
```
#### POST - /api/token/

```
Example Payload:
{
  "email": "user@example.com",
  "password": "string"
}

Example Success Response:
{
  "message": "Operation Success",
  "data": {
    "id": "ef09c3d5-2ca0-4773-842e-a7f2316f0631",
    "role": "U",
    "email": "user@example.com",
    "refresh": "...",
    "access": "..."
  }
}
Example Error Response:
{
  "message": "Client Error",
  "data": {
    "type": "client_error",
    "errors": [
      {
        "code": "no_active_account",
        "detail": "No active account found with the given credentials",
        "attr": null
      }
    ]
  }
}
```
#### POST - /api/token/refresh/

```
Example Payload:
{
  "refresh": "..."
}

Example Success Response:
{
  "message": "Operation Success",
  "data": {
    "access": "..."
  }
}
Example Error Response:
{
  "message": "Client Error",
  "data": {
    "type": "client_error",
    "errors": [
      {
        "code": "token_not_valid",
        "detail": "Token is invalid or expired",
        "attr": "detail"
      },
      {
        "code": "token_not_valid",
        "detail": "token_not_valid",
        "attr": "code"
      }
    ]
  }
}
```
#### GET - /api/mutual-funds/

```
Example  Response:
{
  "message": "Operation Success",
  "data": {
    "results": [
      {
        "id": "e17a3b7f-2b07-4fb7-8cfe-34e3f5c8bbe2",
        "name": "Blue Chip Fund",
        "fund_type": "E",
        "nav": 10
      }
    ],
    "pagination": {
      "current_limit": 10,
      "next": null,
      "previous": null,
      "count": 1,
      "current_page": 1
    }
  }
}
```
#### POST - /api/mutual-funds/

```
Example Payload:
{
  "name": "Blue Chip Fund",
  "fund_type": "E",
  "nav": 10
}
Example  Response:
{
  "message": "Operation Success",
  "data": {
    "id": "e17a3b7f-2b07-4fb7-8cfe-34e3f5c8bbe2",
    "created_at": "2025-01-14T18:50:07.209925Z",
    "modified_at": "2025-01-14T18:50:07.209925Z",
    "name": "Blue Chip Fund",
    "fund_type": "E",
    "nav": 10
  }
}
```
#### PATCH - /api/mutual-funds/{id}/

```
Example Payload:
{
  "nav": 9
}

Example  Response:
{
  "message": "Operation Success",
  "data": {
    "nav": 5
  }
}
```
#### POST - /api/investments/

```
Example Payload:
{
  "units": 1,
  "mutual_fund": "e17a3b7f-2b07-4fb7-8cfe-34e3f5c8bbe2"
}

Example  Response:
{
  "message": "Operation Success",
  "data": {
    "id": "ce3adf21-5934-4fa3-b212-4dfffa07330f",
    "created_at": "2025-01-14T18:52:49.721090Z",
    "modified_at": "2025-01-14T18:52:49.721090Z",
    "units": 1,
    "user": "5f446b3a-e483-4912-be15-b18ecef90825",
    "mutual_fund": "e17a3b7f-2b07-4fb7-8cfe-34e3f5c8bbe2"
  }
}
```
#### GET - /api/investments/

```

Example  Response:
{
  "message": "Operation Success",
  "data": {
    "results": [
      {
        "id": "ce3adf21-5934-4fa3-b212-4dfffa07330f",
        "mutual_fund": "Blue Chip Fund",
        "units": 1
      }
    ],
    "pagination": {
      "current_limit": 10,
      "next": null,
      "previous": null,
      "count": 1,
      "current_page": 1
    }
  }
}
```

#### GET - /api/report/

```

Example  Response:
{
  "message": "Operation Success",
  "data": {
    "results": [
      {
        "mutual_fund": "Blue Chip Fund",
        "total_units": 1,
        "total_value": 5
      }
    ]
  }
}
```

