"""
Name: Rock Paper Scissors
Version: 0.1
Date: 22Mar20

Description:
Practice Program to play with classes and hierarchies
"""

import random

# Constants
ROCK     = 0;
PAPER    = 1;
SCISSORS = 2;

PLAYER_WIN  = 0;
PLAYER_LOSE = 1;
PLAYER_TIE  = 2;

class computerStrategy:
    """ Base class for Computer player

    Attributes:
        lastGuess = The prior guess made by the computer
        currentGuess = The current guess made by the computer
    """
    lastGuess = ""
    currentGuess = ""

    def makeSelection(self):
        """ Use the internally defined AI strategy to make a guess

        Parameters:
            None

        Returns:
             None
        """
        randomSelection = random.randint(ROCK, SCISSORS)
        return randomSelection


def getOutcomeOfGame(playerGuess, computerGuess):
    """ Takes the player's guess and the conputer's guess and returns the player's status

    :param playerGuess: ROCK, PAPER, or SCISSORS
    :param computerGuess: ROCK, PAPER, or SCISSORS
    :return: The result for the player
    """
    resultsArray = [[PLAYER_TIE,  PLAYER_LOSE, PLAYER_WIN],
                    [PLAYER_WIN,  PLAYER_TIE,  PLAYER_LOSE],
                    [PLAYER_LOSE, PLAYER_WIN,  PLAYER_TIE]]
    return resultsArray[playerGuess][computerGuess]


def printGuesses(argPlayerSelection, argComputerSelection):
    """ Takes the numerical values and prints the results
    """
    print("Player played:", end=" ")
    printGuess(argPlayerSelection)
    print("Computer played:", end=" ")
    printGuess(argComputerSelection)


def printGuess(argSelection):
    """ Prints the selection in plain text

    :param argGuess:
    :return:
    """
    textValues = ['Rock', 'Paper', 'Scissors']
    print(textValues[argSelection])


def printResults(argResults):
    """ Takes the results value and prints it out.

    :return:
    """
    if argResults == PLAYER_WIN:
        print("Player Wins!")
    elif argResults == PLAYER_LOSE:
        print("Player Loses!")
    else:
        print("It's a tie!")


def getSelection():
    """ Gets the player's selection

    :return: valid player selection
    """
    validInputs = [0, 1, 2]
    isValid = False
    while isValid is False:
        print('Input your guess (ROCK = 0, PAPER = 1, SCISSORS = 2:', end=" ")
        playerSelectionString = input()
        playerSelectionInt = int(playerSelectionString)
        if playerSelectionInt in validInputs:
            isValid = True

    return playerSelectionInt


def printWelcome():
    print('The player enters a guess and the computer guesses. Results are printed')
    """ Prints the rules for Rock, Paper, Scissors
    """
    print('\n---------------------\nROCK, PAPER, SCISSORS\n---------------------\n')


def askPlayAgain():
    """ Ask the player to play again
    Sanitizes input
    :return: True or False
    """
    print('Do you want to play again? (yes or no): ')
    playAgainBool = input().lower().startswith('y')
    return playAgainBool

"""
MAIN PROGRAM
"""
printWelcome()

playAgain = True
while playAgain == True:
    playerSelected = getSelection()
    computerPlayer = computerStrategy()
    computerSelected = computerPlayer.makeSelection()
    gameResult = getOutcomeOfGame(playerSelected, computerSelected)
    printGuesses(playerSelected, computerSelected)
    printResults(gameResult)
    playAgain = askPlayAgain()


