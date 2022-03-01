mydata = ""
while mydata != "tester":
    mydata = input("enetr a name : ")
    type = {
        "comment": []
    }
    for i in type:
        type["comment"].append(mydata)
    print(type)