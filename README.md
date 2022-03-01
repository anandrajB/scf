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

1. python manage.py makemigrations accounts
2. python manage.py makemigrations transaction
3. python manage.py migrate accounts
4. python manage.py migrate transaction


## TESTING

1. python manage.py test accounts
2. python manage.py test transaction