# DRF-Serializer-Filter-Throttle Example

An Example Django REST framework project for filter data from DB with some API restriction.

## API Endpoints

* **/api/questions/**  (Question list endpoint)
* **/api/questions/{question id}/** (Specific question info endpoint)

## Requirements

* **python==3.*
* **Django==1.11.*
* **django-filter==1.0.4
* **djangorestframework==3.6.4
* **psycopg2==2.7.3.1
* **pytz==2017.2

## Installation

* Create global environment for project

    mkvirtualenv <env_name> (virtualenv)

* Clone project repository in your system and move inside project folder
* Activate virtualenv and install project requirements

    pip install -r requirements.txt

* Run migrations first before loading fixtures

    python manage.py migrate

* Load fixtures data (**Note** :- Only for testing purpose, No need to load on production server)

    python manage.py loaddata fixtures/*

* Create SuperUser incase want to se django default admin panel

    python manage.py createsuperuser

* Run test cases to check all created functionality is working in all scenario

    python manage.py test

## Process to hit API
All api required api_key which generated when we create tenant in DB.
API_KEY is a random no. which identify tenant in system and count API hits made by using API_KEY. It's a url parameter which set with `api_key` key in URL.

    **/api/questions/?api_key={unique_id}**

**Note: Every tenant have API hit limit (100 per day). After threshold limit tenant can hit API after each 10 second (i.e 1 hit per 10 seconds)**

## Operations perform on API
At this time we only GET operation which retrive question table data from DB.
By default if we hit above API then list of question's which are not private will be displayed.

We can search for question by different filter methods

* **/api/questions/?title={value_to_search}&api_key={unique_id}** (Exact match)
* **/api/questions/?title__contains={value_to_search}&api_key={unique_id}** (Contain with case sensitive match)
* **/api/questions/?title__startswith={value_to_search}&api_key={unique_id}** (First value with case sensitive match)
* **/api/questions/?title__icontains={value_to_search}&api_key={unique_id}** (Contain with case insensitive match)

# Default View
Default page contain dashboard which show total record of Questions, Answers, Users and Tenant. Also show total API hit made by tenant
