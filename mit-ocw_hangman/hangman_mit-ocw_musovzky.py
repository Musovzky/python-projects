# hangman_mit-ocw_musovzky.py
# Python version: 3.4.3
# Created by: Musovzky (viviyi4@gmail.com)
# Created on: June 27, 2016

# Hangman is a guessing game between you and your computer...
# You can choose among 3 difficulty levels: Beginner, Intermediate and Savvy

# This is the first project of MIT OpenCourseWare:
# A Gentle Introduction to Programming Using Python
# This program is created from the template provided in the course materials

# Note: A word list (words.txt) and a python interpreter is needed to
# run the program

import string
import random

myFile = open("words.txt", "r")
myWords = myFile.read().split()
print("Loading words...\n")

def getWords():
    while True:
        try:
            num = int(input("> How many words would you like to add to your word list: "))
            if num > 0:
                print(">> Copy that. %i words loaded.\n" %num)
                return random.sample(myWords,num)
                break
            else:
                print("# Be sure to enter an integer greater than 0")
        except ValueError:
            print("# Be sure to enter an integer.")
            continue
            
def chooseLevel():
    print("Please enter 1/2/3 to choose a level."
          "\n - Beginner (1): 8 guesses"
          "\n - Intermediate (2): 6 guesses"
          "\n - Savvy (3): 4 guesses")
    while True:
        myLevel = input("> Choose your level: ")
        if myLevel == "1":
            return 8
            break
        if myLevel == "2":
            return 6
            break
        if myLevel == "3":
            return 4
            break
        else:
            print("# Be sure to enter only 1, 2 or 3.")

def sourceLetters(sourceWord):
    checkList = ""
    for char in sourceWord.lower():
        if char not in checkList:
            checkList += char
    return checkList

def createBlanks(sourceWord):
    for slot in sourceWord:
        sourceWord = sourceWord.replace(slot,"_ ")
    return sourceWord

def updateBlanks(correctLetters,sourceWord):
    for slot in sourceWord:
        if slot.lower() not in correctLetters.lower():
            sourceWord = sourceWord.replace(slot,"_ ")
    return sourceWord

def hangman():

    newGame = True
    while newGame:
        
        myWordList = getWords()
        maxGuess = chooseLevel()
        counter = 0
        winCounter = 0
        total = len(myWordList)

        while myWordList != []:

            secretWord = random.choice(myWordList)
            counter += 1
            guessedLetters = ""
            correctLetters = ""
            mistakesMade = 0
            checkList = sourceLetters(secretWord)
            blanks = createBlanks(secretWord)
            print(">> Secret word %i/%i:" %(counter,total) + blanks)

            while mistakesMade < maxGuess:

                precheck = True
                while precheck:
                    
                    myGuess = input("> Guess a letter: ")

                    # check if valid
                    if myGuess.lower() not in string.ascii_lowercase:
                        print("# Be sure to enter a letter from A(a) to Z(z).")

                    # check if duplicate
                    elif myGuess in guessedLetters:
                        print("# Please enter a new letter.")
                        
                    else:
                        guessedLetters += myGuess
                        break

                # if correct
                if myGuess.lower() in checkList:
                    checkList = checkList.replace(myGuess.lower(),"")
                    correctLetters += myGuess
                    print(">> " + updateBlanks(correctLetters,secretWord))
                    
                    if checkList != "":
                        print(">> You get it! Now keep going.")
                    else:
                        print(">> Congrats! You win.")
                        myWordList.remove(secretWord)
                        winCounter += 1
                        break
                    
                # if incorrect
                else:
                    mistakesMade += 1
                    livesLeft = maxGuess - mistakesMade
                    
                    if livesLeft > 1:
                        print(">> Oops... Maybe you should give another try.")
                        print("   %i lives left." %livesLeft)
                    elif livesLeft == 1:
                        print(">> Oops... Maybe you should give another try.")
                        print("   This is your ONE last chance!")
                    else:
                        print(">> Do you hear the people sing? Singing the song of hangman.")
                        print("   The secret word is " + secretWord)
                        myWordList.remove(secretWord)
                        break

            # decide whether or not to start a new round
            if counter < total:
                newRound = input("> Press any key other than N to continue: ")
                if newRound == "N" or newRound == "n":
                    print(">> Hope you had fun!")
                    break
                else:
                    print(">> Good luck with it!")
                    
        print("That's the end of the game.")
        print("You win %i out of %i." %(winCounter,counter))

        # decide whether or not to start a new game
        while True:
            startNewGame = input("> Would you like to start a new Game (Y/N): ")
            if startNewGame == "Y" or startNewGame == "y":
                newGame = True
                break
            elif startNewGame == "N" or startNewGame == "n":
                newGame = False
                break
            else:
                print("# Be sure to enter only 'Y(y)' or 'N(n)'.")
                    
hangman()
