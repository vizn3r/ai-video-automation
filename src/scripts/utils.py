GREEN = "\033[92m"
RED = "\033[91m"
END = "\033[0m"

def Info(*message):
    print(GREEN + "==>", *message, END)

def Error(*message):
    print(RED + "==!", *message, END)

def Except(e, *message):
    print("[ EXCEPTION ]", *message, "\n  >>>", e)

def CheckMain():
    if __name__ == "__main__":
        Error("This script is not meant to run standalone")
        exit(0)

CheckMain()