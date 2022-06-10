import urllib.request, json 
arr1 = []
qs = []
with urllib.request.urlopen("https://openexchangerates.org/api/currencies.json") as url:
    data = json.loads(url.read().decode())
    for key,values in data.items():
        arr1.append(key)
    for (i,j) in zip(range(1,len(arr1)), arr1) :
        data = {
        "model": "accounts.currencies",
        "pk": i,
        "fields": {
            "iso": 784,
            "description": j
            }
        }
        qs.append(data)
        jsonstring = json.dumps(qs)
    print(jsonstring)
