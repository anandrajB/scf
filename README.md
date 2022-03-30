# SCF_BACKEND

# BUILD WITH DJANGO==3.2.5 LTS


## INSTALLATION AND RUNNING 

1. pip install -r requirements.txt
2. python manage.py migrate
3. python manage.py migrate --run-syncdb
4. python manage.py runserver

## TENANT PROCESS

1. python manage.py migrate_schemas  ( for schmeas migration )
2. python manage.py create_tenant_superuser  ( superuser for tenant's )


## NEW DB CONFIG (POSTGRES)

1. python manage.py migrate 
2. python manage.py makemigrations 
3. python manage.py migrate silk zero { for performance review }

## DUMP TEST DATA

1. python manage.py loaddata accounts.json
2. python manage.py loaddata transactions.json
3. python manage.py loaddata currencies.json
4. python manage.py loaddata countries.json

## TABLE DATA'S DUMPING - PRODUCTION

1. heroku run -a venzoscf python manage.py loaddata accounts.json
2. heroku run -a venzoscf python manage.py loaddata fixtures -l > data.json

## TESTING

1. python manage.py test accounts
2. python manage.py test transaction


## POSTMAN LINKS FOR API TESTING

1. https://www.getpostman.com/collections/74a150a6a4ee22543b8c


## POSTMAN DOCUMENTATION LINK

1. https://web.postman.co/workspace/b73d75d6-d290-4c8a-89f4-0f112accd87d/documentation/11858287-a66d8d10-fe32-4075-bd9b-26ae05df5402


## HEROKU URL

1. https://venzoscf.herokuapp.com/

## QUERY PERFORMANCE AND RESPONSE

1. https://venzoscf.herokuapp.com/silk/


## API END_POINTS


1. https://venzoscf.herokuapp.com/api-urls/


