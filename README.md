# SCF_BACKEND

# BUILD WITH DJANGO==3.2.5 LTS


## INSTALLATION AND RUNNING **

1. pip install -r requirements.txt
2. python manage.py migrate
3. python manage.py migrate --run-syncdb
4. python manage.py runserver

## TENANT PROCESS 

1. python manage.py migrate_schemas  ( for schmeas migration )
2. python manage.py create_tenant_superuser  ( superuser for tenant's )


## NEW DB CONFIG (POSTGRES) **

1. python manage.py migrate 
2. python manage.py makemigrations 
3. python manage.py migrate --run-syncdb

## DUMP TEST DATA 

#### test credentials 
1. python manage.py loaddata fixtures/accounts.json
2. python manage.py loaddata fixtures/transactions.json

#### misc
3. python manage.py loaddata fixtures/actions.json   
4. python manage.py loaddata fixtures/currencies.json
5. python manage.py loaddata fixtures/countries.json

## TABLE DATA'S DUMPING - TESTING

1. heroku run -a venzoscf python manage.py loaddata fixtures/data.json
2. heroku run -a venzoscf python manage.py loaddata fixtures/actions.json

## RUNNING TEST CASES **

1. python manage.py test accounts
2. python manage.py test transaction

## DB DIAGRAM

1. https://dbdiagram.io/d/61b82d3b8c901501c0ef1a4f


## POSTMAN COLLECTION FOR API TESTING

1. https://www.getpostman.com/collections/74a150a6a4ee22543b8c


## DOCUMENTATION LINK

1. https://documenter.getpostman.com/view/11858287/Uyr5pf1h


## HOME URL

1. https://venzoscf.herokuapp.com/

## ADMIN PANEL  

1. https://venzoscf.herokuapp.com/admin/


## ADMIN CREDENTIALS **

***phone*** : 1471471471\
***password*** : admin123\
***email*** : finflo@admin.com\
**test purpose only


## API END_POINTS

1. https://venzoscf.herokuapp.com/api-urls/





### ***NOTE 1*** : The ** indicated one are important and required commands

### ***NOTE 2*** : Before running this project , check PRODUCTION.md file



## WORKING ENVIRONMENTS

1. TESTING    :  http://venzoscf.herokuapp.com

2. PRODUCTION :  http://206.189.129.55/