from accounts.models import Currencies , Countries , Parties
from transaction.models import Pairings
 


# FUNCTION'S FOR GETTING THE VALUES AFTER INVOICE BULK UPLOAD - final_state == YES

def gets_currencies(values):
    return Currencies.objects.get(id = values)
    
def gets_party(id):
    query = Parties.objects.get(name  = id)
    return query
     
def gets_pairings(id):
    cs = Pairings.objects.get(id=id)
    return cs

