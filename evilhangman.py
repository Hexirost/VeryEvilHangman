import pprint
import copy
from tools import setToFullLetterMaskIndex, greedyAlgo

f = open(r"mini.txt")
words = f.read()
ALPHABET = set(chr(x) for x in range(97,123))

wordSet = set(words.split("\n"))
attemptedLetters = set()
gameState = ["_"] * 4

FLMI = setToFullLetterMaskIndex(wordSet, set())
while True:
    print("Attempted = {}".format(attemptedLetters))
    print("Puzzle: ",end = "")
    for pos in gameState:
        print(pos + "", end = " ")
    userGuess = input("\nPlease enter a letter to guess: ")
    
    if not userGuess.isalpha() or userGuess.lower() in attemptedLetters:
        print("Invalid guess please try again\n")
    userGuess = userGuess.lower()

    print("Greedy is {}".format(greedyAlgo(userGuess, gameState, FLMI)))
