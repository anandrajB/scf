from rest_framework.response import Response
from accounts.models import Parties , signatures 
from transaction.models import Programs, workflowitems
from accounts.models import Currencies  , Parties
from transaction.models import Pairings
from rest_framework.exceptions import APIException



### ABOUT THIS FILE ###

# This query_handler.py checks all the signatures for  each action button in all scenario's




# ---------------------#
# PROGRAM QUERIES      #
# ---------------------#


### FUNCTION FOR SUBMIT SIGNATURES BASED ON USER_TYPE i.e., bank / customer ###

def submit_transition(request):
    user = request.user
    bank = Parties.objects.get(party_type="BANK")
    if user.party.party_type == "BANK":
        obj = signatures.objects.get(party=bank, action__desc__contains="SUBMIT", model="PROGRAM")
    else:
        obj = signatures.objects.get(party=user.party, action__desc__contains="SUBMIT", model="PROGRAM")
    return obj


### SIGNATURES FUNCTION FOR REJECT SIGNATURES BASED ON USER_TYPE i.e ., bank / customer ###

def reject_transition(request):
    user = request.user
    bank = Parties.objects.get(party_type="BANK")
    if user.party.party_type == "BANK":
        obj = signatures.objects.get(party=bank, action__desc__contains="REJECT", model="PROGRAM")
    else:
        obj = signatures.objects.get(party=user.party, action__desc__contains="REJECT", model="PROGRAM")
    return obj


# FUNCTION FOR GETTING CURRENT LOGGED-IN USER
def myuser(request):
    return request.user


### FUNCTION GETS wf_item_id (COMMON) ###

def gets_wf_item_id(id):
    return workflowitems.objects.get(id=id)


#### SIGNATURE FUNCTION FOR ACCEPT TRANSITION FOR CUSTOMER ###

def accept_transition(request):
    user = request.user.party
    if user.party_type == "BUYER":
        obj = signatures.objects.get(party=user, action__desc__contains="ACCEPT", model="PROGRAM") 
    return obj


### SIGNATURE FUNCTION FOR APPROVE TRANSITION FOR BANK ###

def approve_transition(request):
    user = request.user.party.party_type
    bank = Parties.objects.get(party_type="BANK")
    if user == "BANK":
        obj = signatures.objects.get(party=bank,  action__desc__contains="APPROVE", model="PROGRAM")
    return obj





# ---------------------#
# INVOICE UPLOAD QUERY #
# ---------------------#

###  INVOICE UPLOAD ###

def upload_submit_transitions(request):
    user = request.user.party
    return signatures.objects.get(party=user, action__desc__contains="SUBMIT", model="UPLOAD")

def gets_currencies(values):
    return Currencies.objects.get(description = values)
    
def gets_party(id):
    query = Parties.objects.get(name  = id)
    return query
     
def gets_pairings(id):
    cs = Pairings.objects.get(id=id)
    return cs

def gets_programs(id):
    qs = Programs.objects.filter(id = id)
    return qs


# ---------------------#
# INVOICE  QUERY       #
# ---------------------#



### Function to APPROVE for user type "BUYER" ###

def invoice_approve_transition(request):
    user = request.user
    if user.party.party_type == "BUYER":
        qs = signatures.objects.get(party=user.party, action__desc__contains="APPROVE", model="INVOICE")
    return qs


### Function to REQUEST FINANCE for user type "SELLER" ###

def reqFin_transition(request):
    user = request.user
    if user.party.party_type == "SELLER":
        obj = signatures.objects.get(
            party=user.party, action__desc__contains="REQUEST FINANCE", model="INVOICE")

    return obj


### Function to SUBMIT for user type "SELLER" ###

def invoice_submit_transition(request):
    user = request.user
    if user.party.party_type == "SELLER":
        obj = signatures.objects.get(party=user.party, action__desc__contains="SUBMIT", model="INVOICE")
    return obj


### Function to REJECT for user type "BUYER" ###

def invoice_reject_transition(request):
    user = request.user
    if user.party.party_type == "BUYER":
        obj = signatures.objects.get(party=user.party, action__desc__contains="REJECT", model="INVOICE")
    return obj



# ------------------------------#
#    INVOICE QUERY FOR BANKS    #
# ------------------------------#


# Function to APPROVE for user type "BANK"

def bank_approve_transition(request):
    user = request.user
    bank = Parties.objects.get(party_type='BANK')
    try:
        qs = signatures.objects.get(party=bank, action__desc__contains="APPROVE", model="INVOICE")
        return qs
    except:
        raise APIException("signatures data not found")

# Function to REJECT for user type "BANK"

def bank_reject_transition(request):
    user = request.user
    bank = Parties.objects.get(party_type='BANK')
    if user.party.party_type == "BANK":
        obj = signatures.objects.get(
            party=bank, action__desc__contains="REJECT", model="INVOICE")

    return obj


# Function to SETTLE for user type "BANK"

def bank_settle_transition(request):
    user = request.user
    bank = Parties.objects.get(party_type='BANK')
    if user.party.party_type == "BANK":
        obj = signatures.objects.get(
            party=bank, action__desc__contains="SETTLE", model="INVOICE")

    return obj

# Function to OVERDUE for user type "BANK"

def bank_overdue_transition(request):
    user = request.user
    bank = Parties.objects.get(party_type='BANK')
    if user.party.party_type == "BANK":
        obj = signatures.objects.get(
            party=bank, action__desc__contains="OVERDUE", model="INVOICE")

    return obj
