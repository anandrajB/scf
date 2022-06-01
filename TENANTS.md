## BEFORE USING TENANTS


#### navigate to scfadmin/settings.py
1. check the debug is set TRUE in settings.py
2. clearly go a walkthrough with settings.py 
3. a detailed note for the tenant process settings has been updated in settings.py 


## TENANT CONFIGURATION

1. The client Folder maintains all the tenant models and creation { ***important :*** don't edit or delete }
2. In  settings.py comment ***INSTALLED APPS***  section , and uncomment the ***TENANT CONFIG'S*** section.
3. In Line no.145 , you can find the ***MIDDLEWARE*** section and now uncomment the first line of that section.
