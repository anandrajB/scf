ss = 1
while ss<5:
    a = input("enter a name")
    car = {
    "data": "Ford",
    }
    for i in a:
        d = {"color": a}
        car.update(d)

    print(car)
    