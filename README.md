# SCF_BACKEND

# build with django==3.2.5 LTS


# installation and running 

1. pip install -r requirements.txt
2. python manage.py migrate
3. python manage.py migrate --run-syncdb
4. python manage.py runserver

# tenant process

1. python manage.py migrate_schemas  ( for schmeas migration )
2. python manage.py create_tenant_superuser  ( superuser for tenant's )


