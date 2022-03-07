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


## API END_POINTS



<!-- api-auth/
api/ program/ [name='program-create-api']
api/ program/<int:pk>/ [name='program-update']
api/ invoice/ [name='invoice-manual-create-api']
api/ invoice/<int:pk>/ [name='invoice-update']
api/ ^invoiceupload/$ [name='invoiceuploads-list']
api/ ^invoiceupload\.(?P<format>[a-z0-9]+)/?$ [name='invoiceuploads-list']
api/ ^$ [name='api-root']
api/ ^\.(?P<format>[a-z0-9]+)/?$ [name='api-root']
api/ invoiceupload/<int:pk>/ [name='invoiceupload-update']
api/ pairing/ [name='pairing-create-list']
api/ pairing/<int:pk>/ [name='pairing-update']
api/ program/transition/delete/<int:pk>/ [name='delete-transition']
api/ program/transition/submit/<int:pk>/ [name='initial-submit-transition-SUBMIT']
api/ program/transition/reject/<int:pk>/ [name='initial-reject-transition-REJECT']
api/ program/transition/accept/<int:pk>/ [name='initial-accept-transition-ACCEPT']
api/ program/transition/approve/<int:pk>/ [name='initial-approve-transition-APPROVE-bank_user']
api/ program/transition/return/<int:pk>/ [name='program-return-RETURN']
api/ program/transition/submit/
api/ program/transition/reject/
api/ program/transition/accept/
api/ program/transition/approve/
api/ invoice/transition/approve/<int:pk>/ [name='invoice-approve-transition']
api/ invoice/transition/submit/<int:pk>/ [name='initial-submit-transition']
api/ invoice/transition/reject/<int:pk>/ [name='initial-reject-transition']
api/ invoice/transition/archive/<int:pk>/ [name='initial-archeive-transition']
api/ invoice/transition/RF/<int:pk>/ [name='initial-request-finance-transition']
api/ invoice/transition/submit/
api/ invoice/transition/reject/
api/ invoice/transition/approve/
api/ invoice/transition/RF/
api/ invoice/transition/archive/
api/ invoiceupload/transition/submit/<int:pk>/ [name='invoice-upload-submit']
api/ invoiceupload/transition/submit/
api/ messages/ -->


