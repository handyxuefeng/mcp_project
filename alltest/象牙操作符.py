x = 10
y = 30


def getdata():
    return 1 == 1


data = getdata()
if data:
    print("data is ", data)


"""
data := getdata():
等价于
data = getdata()
if data:
    print("data is ", data)

"""
if data := getdata():
    print("data is ", data)
