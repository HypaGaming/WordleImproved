from PyDictionary import PyDictionary

d = PyDictionary()

def define(word):  # Defining the word using PyDictionary

    definition = str(d.meaning(word, True))  # Getting original definition w/out formatting
    alChar = "abcdefghijklmnopqrstuvwxyz:, ".upper()  # The characters that are allowed in definition

    for i in range(len(definition)):
        if definition[i].upper() not in alChar:
            definition = definition.replace(definition[i], " ") # Replace illegal characters in string

    definition = " ".join(definition.split())

    if definition == 'None':
        definition = 'No Definition Found'

    print(definition)



while  True:
    word = input("Word for definition: ")
    define(word)