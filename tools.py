def setToFullLetterMaskIndex(wordSet, usedLetters = set()):
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
    if mask == (-1,):
        return gameState
    for pos in mask:
        if gameState[pos] == "_":
            gameState[pos] = letter
        else:
            print("what the hell?")
    return gameState


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
        letterMaskDict = setToFullLetterMaskIndex(set(chosenList))
        outer_max_lengths = {
            k: max(len(inner_val) for inner_val in v.values())
            for k, v in letterMaskDict.items()
        }
        nextGuess = min(outer_max_lengths, key=outer_max_lengths.get)
    if len(chosenList) == 1 and "_" in newGameState:
        count += newGameState.count("_")

    return count, fails