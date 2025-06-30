from copy import deepcopy
from itertools import chain

ALPHABET = set(chr(x) for x in range(97,123))

def fileToSet(filename):
    f = open(filename)
    words = f.read()

    wordSet = set(words.split("\n"))
    return wordSet

def setToLetterMaskIndex(wordSet, usedLetters = set()):
    res = {}
    wordSet = set(wordSet)
    ''' For every word in set add it to a dictionary with a dictionary full of letters and a dictionary full of mask with a list of valid words with that mask format below
    fullDict[Letter:{}][Mask:{}]=[List of valid words using the letter and mask]'''
    for word in wordSet: 
        wordDict = {}
        for index, letter in enumerate(word):
            wordDict.setdefault(letter, []).append(index)
        for letter, positions in wordDict.items():
            res.setdefault(letter, {}).setdefault(tuple(positions),[]).append(word)
    letterSet = set(res.keys()).difference(usedLetters) # Remove used Letters

    # Adding the nullset to -1
    for letter in letterSet:
        wordsWithLetter = set()
        for wordList in res[letter].values():
            wordsWithLetter.update(wordList)
        nullSet = wordSet.difference(wordsWithLetter)
        if len(nullSet) > 0:
            res[letter][(-1,)] = nullSet

    return res

def updateGameState(letter,mask,gameState):
    newGameState = gameState[:]
    if mask == (-1,):
        return newGameState
    for index, blank in enumerate(newGameState):
        if blank != "_" and index in mask:
            return False
    for pos in mask:
        if newGameState[pos] == "_":
            newGameState[pos] = letter
        else:
            print("what the hell?")
    return newGameState


def greedyAlgo(nextGuess, gameState, letterMaskDict):
    '''
    Greedy approach for finding the best solution; it will always pick option with the most remaining words
    '''
    count, fails = 0, 0
    chosenList = []
    chosenMask = (-2,)
    newGameState = gameState[:]
    while "_" in newGameState and len(chosenList) != 1:
        count += 1
        masksForWord = letterMaskDict[nextGuess]
        chosenMask, chosenList = max(masksForWord.items(), key = lambda kv: len(kv[1]))
        print("Here",count, nextGuess, chosenList, chosenMask)
        if chosenMask == (-1,):
            fails+=1
        newGameState = updateGameState(nextGuess, chosenMask, newGameState)
        if newGameState == False:
            continue
        letterMaskDict = setToLetterMaskIndex(set(chosenList))
        outer_max_lengths = {
            k: max(len(inner_val) for inner_val in v.values())
            for k, v in letterMaskDict.items()
        }
        nextGuess = min(outer_max_lengths, key=outer_max_lengths.get)
    if len(chosenList) == 1 and "_" in newGameState:
        count += newGameState.count("_")

    return count, fails

def veryEvilAlgo(currGuess, gameState, FLMI, attemptedLetters):
    attempts = []
    def helperEvilAlgo(currGuess, gameState, FLMI, attemptedLetters):
        nonlocal attempts
        attemptedLetters.append(currGuess)

        if currGuess not in FLMI or len(attemptedLetters) == 26:
            return None
        blanks = gameState.count("_")
        if  blanks == 0:
            attempts.append((attemptedLetters, gameState, len(attemptedLetters) - (4-blanks)))
            return None
        elif blanks == 1:
            possibleWords = set(chain.from_iterable(list(v.values())[0] for v in FLMI.values()))
            for letters in possibleWords:
                attempts.append((attemptedLetters, letters, len(possibleWords)-1 + len(attemptedLetters) - (4-blanks))) 
            return None

        for mask in deepcopy(FLMI)[currGuess].items():
            maskPos, wordsForMask = mask
            if len(wordsForMask) == 1:
                attempts.append((attemptedLetters, wordsForMask, len(attemptedLetters) - (4-blanks)))
                return None
            newGameState = updateGameState(currGuess,maskPos,gameState)
            if newGameState == False:
                return None
            newFLMI = setToLetterMaskIndex(wordsForMask)
            for newLetter in ALPHABET.difference(set(attemptedLetters)):
                newAttempt = helperEvilAlgo(newLetter, deepcopy(newGameState), deepcopy(newFLMI), deepcopy(attemptedLetters))
                if newAttempt == None:
                    continue
            
    helperEvilAlgo(currGuess, gameState, FLMI, attemptedLetters)
    return attempts
