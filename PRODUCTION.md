## BEFORE PRODUCTION REMEDIES

1. check the debug is set TRUE in settings.py
2. managing static and staticfiles for root directory
3. keep .env secret { ***important :*** don't edit or delete }


## DATABASE CONFIGURATION

1. check the settings.py file in scfadmin/settings.py
2. In  ***DATABASE SETUP***  section , you can find setup .
3. for production , set ***PRODUCTION = True*** in settings.py (line no.34)
4. for running locally using local postgres database you can uncomment the setup 2 and comment the setup 1 sections . 

5. **NOTE*** : before using atleast any one of the setup in ***DATABASE SETUP*** section is need to be commented out