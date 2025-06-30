from tools import setToLetterMaskIndex, greedyAlgo, veryEvilAlgo, fileToSet
wordSet = fileToSet(r"mini.txt")
attemptedLetters = []
gameState = ["_"] * 4
LMI = setToLetterMaskIndex(wordSet, set())

while True:
    print("Attempted = {}".format(attemptedLetters))
    print("Puzzle: ",end = "")
    for pos in gameState:
        print(pos + "", end = " ")
    userGuess = input("\nPlease enter a letter to guess: ")
    
    if not userGuess.isalpha() or userGuess.lower() in attemptedLetters:
        print("Invalid guess please try again\n")
        continue
    userGuess = userGuess.lower()
    print("Greedy is {}".format(greedyAlgo(userGuess, gameState, LMI)))
    res = veryEvilAlgo(userGuess, gameState, LMI, attemptedLetters)

