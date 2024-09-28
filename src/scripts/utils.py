def Info(*message):
    print("[ INFO ]", *message)

def Error(*message):
    print("[ ERROR ]", *message)

def Except(e, *message):
    print("[ EXCEPTION ]", *message, "\n  >>>", e)
