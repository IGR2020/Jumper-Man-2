from Game.objects import *

objectMap = {"g": Object, "b": Object, "s": Object, "i": Object, "f": Fire}
objectAssetMap = {"g": "Grass Block", "b": "Grass Block", "s": "Spike", "i": "Ice Block"}
objectTypeMap = {"g": "Object", "b": "Object", "s": "Trap", "i": "Object", 'f': "Trap"}

def loadLevel(path) -> tuple[list, list[int, int]]:
    with open(path, "r") as file:
        data = file.read()
        file.close()
    
    objects = []
    levelSize = [0, len(data.splitlines())*blockSize]

    for i, line in enumerate(data.splitlines()):
        for j, char in enumerate(line):

            if char in ";:, ":
                continue

            if j*blockSize > levelSize[0]:
                levelSize[0] = j*blockSize

            if objectMap[char].__name__ == "Fire":
                objects.append(objectMap[char](j*blockSize, i*blockSize))
            else:
                objects.append(objectMap[char](j*blockSize, i*blockSize, objectAssetMap[char], type=objectTypeMap[char]))

            if objectTypeMap[char] == "Trap":
                objects[-1].rect.bottom = (i+1)*blockSize
                objects[-1].rect.centerx = j*blockSize+blockSize/2

    return objects, levelSize