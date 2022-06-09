import os
from django.core.exceptions import ValidationError


# CUSTOM FILE VALIDATOR FOR INVOICE CSV UPLOAD 

def validate_invoice_extension(value):
    ext = os.path.splitext(value.name)[1]  
    invoice_extensions = ['.csv','.xlsx']
    if not ext.lower() in invoice_extensions:
        raise ValidationError('Unsupported file extension. Must be in .csv or .xlsx format')



# PROGRAM , INVOICE , COUNTERPARTY ATTACHMENT VALIDATOR


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1] 
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls','.csv']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Supported file extension as .pdf .csv .xlsx .xls .jpg .png ')