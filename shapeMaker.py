import struct


rawInput = ""
f = open("shapes.bin", "r+b")
changesMade = False
shapes = []
addedShapes = []

def getNewPiece():
    current = ""
    try:
        for i in range(2):
            rawInput = input().strip()
            if rawInput == "-e": return 1
            if len(rawInput) != 4:
                print("Wrong input. Try again.")
                return 2
            current += rawInput
        print("Choose the spinpoint from 0 to 22")
        rawInput = input().strip()
        if rawInput == "-e": return 1
        spinpoint = int(rawInput)
        addedShapes.append((int(current, 2), spinpoint))
        global changesMade
        changesMade = True
        print("shape submitted. Input another shape or print -e to exit")
        return 0
    except:
        print("Wrong input! Try again!")


def pieceAddition():
    print("input pieces shapes in following format: \nXXXX\nXXXX\n")
    print("enter -e to go to main menu at any moment.")
    status = 0
    while status != 1:
        status = getNewPiece()

def clearList():
    shapes.clear()
    f.truncate(0)
    print("list cleared")
    global changesMade
    changesMade = True


def applyChanges():
    data = b""
    for num in addedShapes:
        print("adding new stuff")
        data += struct.pack("B", num[0])
        data += struct.pack("B", num[1])
    f.write(data)


def getData():
    content = f.read()
    if len(content) == 0: return 1
    for i in range(0, len(content), 2):
        stuff = struct.unpack("=BB", content[i:i + 2])
        shapes.append(stuff)
    return 0


def showShapes():
    for shape in shapes:
        num = bin(shape[0])[2:10].zfill(8)
        print(f"{num[:4]}\n{num[4:]}\n")
    
def idle():
    while True:
        print("enter command:")
        print("-a: add a new piece to list")
        print("-c: clear the list of pieces")
        print("-e to exit")
        rawInput = input().strip()
        match rawInput:
            case "-a":
                pieceAddition()
            case "-c":
                clearList()
            case "-e":
                print(changesMade)
                if changesMade:
                    applyChanges()
                return 1
            case _: print("Unsupported option! Enter a supported command.")
    return 0

def start():
    print("Greetings at Tetris Shape Editor!")
    getData()
    print("current shapes list:")
    showShapes()
    idle()
    f.close()


start()
