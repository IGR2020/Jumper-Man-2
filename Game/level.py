from Game.objects import *

objectMap = {"g": Object, "b": Object, "s": Object, "i": Object, "f": Fire}
objectAssetMap = {"g": "Grass Block", "b": "Grass Block", "s": "Spike", "i": "Ice Block"}
objectTypeMap = {"g": "Object", "b": "Object", "s": "Trap", "i": "Object"}

def loadLevel(path):
    with open(path, "r") as file:
        data = file.read()
        file.close()
    
    objects = []

    for i, line in enumerate(data.splitlines()):
        for j, char in enumerate(line):
            if char in ";:, ":
                continue
            if objectMap[char].__name__ == "Fire":
                objects.append(objectMap[char](j*blockSize, i*blockSize))
                continue                
            objects.append(objectMap[char](j*blockSize, i*blockSize, objectAssetMap[char], type=objectTypeMap[char]))

    return objects