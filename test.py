import urllib.request, json 
arr = []
i = 1
with urllib.request.urlopen("https://openexchangerates.org/api/currencies.json") as url:
    data = json.loads(url.read().decode())
    for key in data.keys():
        arr.append(key)
    print(len(arr))
    print(arr[0])
    for i in range(i,arr):
        data = {
        "model": "accounts.currencies",
        "pk": arr[i],
            "fields": {
            "iso": 784,
            "description": "AED"
            }
        }