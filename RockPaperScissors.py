#!/usr/bin/env python3

import time
import random

class Player(object):
    # Rock, Paper, Scissors, Total
    previously_played = [0, 0, 0, 0]

    percent_prev_played = [0.0, 0.0, 0.0]

    # Tracks what the player lost to
    regret_play = [0.0, 0.0, 0.0]

    player_name = ''

    games_played = 0

    def __init__(self):
        #TODO access the data base
        self.menu = MenuPrinter()

    def inputPlayerName(self):
        self.player_name = input('What is your name? ')

    def addGamesPlayed(self):
        self.games_played += 1

    def calculatePercentagePreviouslyPlayed(self):
        try:
            prev_rock = (self.previously_played[0]/ self.previously_played[3])
        except ZeroDivisionError:
            prev_rock = 0.0
            print(f'Error {prev_rock}')
        try:
            prev_paper = (self.previously_played[1]/ self.previously_played[3])
        except ZeroDivisionError:
            prev_paper = 0.0
            print(f'Error {prev_paper}')
        try:
            prev_scissors = (self.previously_played[2]/ self.previously_played[3])
        except ZeroDivisionError:
            prev_scissors = 0.0
            print(f'Error {prev_scissors}')
        self.percent_prev_played = [prev_rock, prev_paper, prev_scissors]
    
    def storeChoice(self, played):
        self.played = played
        if played == '1' or played == 'rock':
            self.previously_played[0] += 1
        elif played == '2' or played == 'paper':
            self.previously_played[1] += 1
        elif played == '3' or played == 'scissors':
            self.previously_played[2] += 1
        self.previously_played[3] = self.previously_played[3] + 1
    
    def calculateRegret(self):
        print(f'Games Played: {self.games_played}')
        if self.played == '1' or self.played == 'rock':
            self.regret_play[1] += 1 
            print(f'{self.regret_play[1]} / {self.games_played}')
            self.regret_play[1] = self.regret_play[1] / self.games_played
        elif self.played == '2' or self.played == 'paper':
            self.regret_play[2] += 1
            print(f'{self.regret_play[2]} / {self.games_played}')
            self.regret_play[2] = self.regret_play[2] / self.games_played
        elif self.played == '3' or self.played == 'scissors':
            self.regret_play[0] += 1 
            print(f'{self.regret_play[0]} / {self.games_played}')
            self.regret_play[0] = self.regret_play[0] / self.games_played
        else:
            print('Regret could not be calculated')

    def play(self):
        self.menu.prettyDisplay(f'You played {self.played.capitalize()}')
        self.addGamesPlayed()
        

class Bot(object):

    def __init__(self):
        self.menu = MenuPrinter()
    
    def considerOpRegret(self, player_regret):
        try:
            # player_regret[0] = rock, player_regret[1] = paper, player_regret[2] = scissors
            if player_regret[0] > player_regret[1] or player_regret[0] > player_regret[2]:
                self.play('paper')
            elif player_regret[1] > player_regret[0] or player_regret[1] > player_regret[2]:
                self.play('scissors')
            elif player_regret[2] > player_regret[0] or player_regret[2] > player_regret[1]:
                self.play('rock')
            else:
                self.randomPlay()
        except TypeError:
            self.randomPlay()

    def randomPlay(self):
        bot_choice = random.randint(1,3)
        if bot_choice == 1:
            self.play('rock')
        if bot_choice == 2:
            self.play('paper')
        if bot_choice == 3:
            self.play('scissors')

    def play(self, rps):
        self.menu.prettyDisplay(f'Opponent played {rps.capitalize()}')
        self.played = rps
        return rps


class Game(object):
    gameState = '' # From Players perspective i.e. if the player won gameState would equal 'win'
    gamesPlayedInCurrentSession = 0

    def __init__(self):
        self.player = Player()
        self.bot = Bot()
        self.menu = MenuPrinter()

    def outcome(self):
        if self.player.played == '1' or self.player.played == 'rock':
            if self.bot.played == 'rock':
                self.gameState = 'draw'
            elif self.bot.played == 'paper':
                self.gameState = 'loss'
            elif self.bot.played == 'scissors':
                self.gameState = 'win'
            else:
                print('Something Broke in Outcome')
                exit()
        elif self.player.played == '2' or self.player.played == 'paper':
            if self.bot.played == 'rock':
                self.gameState = 'win'
            elif self.bot.played == 'paper':
                self.gameState = 'draw'
            elif self.bot.played == 'scissors':
                self.gameState = 'loss'
            else:
                print('Something Broke in Outcome')
                exit()
        elif self.player.played == '3' or self.player.played == 'scissors':
            if self.bot.played == 'rock':
                self.gameState = 'loss'
            elif self.bot.played == 'paper':
                self.gameState = 'win'
            elif self.bot.played == 'scissors':
                self.gameState = 'draw'
            else:
                print('Something Broke in Outcome')
                exit()
        else:
            print('Something Broke in Outcome')
            print(f'Player Played: {self.player.played}')
   
    def displayGameState(self):
        self.outcome()
        if self.gameState == 'win':
            self.menu.prettyDisplay('You win! :D')
        if self.gameState == 'loss':
            self.menu.prettyDisplay('You lose! :(')
        if self.gameState == 'draw':
            self.menu.prettyDisplay('It\'s a draw!')
    
    def gameEnd(self):
        self.displayGameState()
        self.player.calculateRegret()
        self.displayEndGameStats()
        self.addOneToPlayedThisSession()
 
    def displayEndGameStats(self):
        self.menu.prettyDisplay(f'End Game Stats\n--- --- ---\nPercent Previously Played: {self.player.percent_prev_played}\nPlayer Regret Percentage:  {self.player.regret_play}')
    
    def addOneToPlayedThisSession(self):
        self.gamesPlayedInCurrentSession += 1


class MenuPrinter(object):

    rock_paper_scissors = {
        1: 'Rock',
        2: 'Paper',
        3: 'Scissors',
    }

    start_menu = {
        'header': 'Are you ready to play?',
        1: 'Yes',
        2: 'No',
    }

    def displayMenu(self, menu, statement):
        rerun = True 
        found_value = False
        while rerun == True:
            print()
            rerun = False
            if 'header' in menu:
                print(menu['header'])
                menu.pop('header')
            for key in menu:
                print(f'{key}.) {menu[key]}')
            choice = input(statement)
            try:
                choice = int(choice)
            except ValueError:
                choice = str(choice).lower()
                for key, value in menu.items():
                    if choice == menu[key].lower():
                        print(f'You chose {value.lower()}.')
                        found_value = True
                if found_value == False:
                    print('Please enter a valid selection')
                    rerun = True
            try:
                choice = menu[choice].lower()
            except KeyError:
                rerun = True
        print()
        return choice

    def prettyDisplay(self, statement):
        print('________________________')
        print()
        print(statement)
        print('________________________')

def main():
    replay = True
    # --{ INIT Classes}--
    game = Game()
    rpsMenu = MenuPrinter()
    #startMenu = MenuPrinter()
    #startMenu.displayMenu(startMenu.start_menu, '')
    try:
        while replay == True:
            
            print() # For spacing before game start

            #time.sleep(1)
            print('Rock\n')

            #time.sleep(1)
            print('Paper\n')

            #time.sleep(1)
            print('Scissors\n')

            #time.sleep(1)
            print('Shoot')

            last_played = str(rpsMenu.displayMenu(rpsMenu.rock_paper_scissors, 'Pick Rock, Paper, or Scissors: '))
            game.player.calculatePercentagePreviouslyPlayed()
            game.player.storeChoice(last_played)
            game.player.play()

            game.bot.considerOpRegret(game.player.regret_play)
            game.gameEnd()
            input('Press enter to play again!')
    except KeyboardInterrupt:
        print('\n\nGoodbye! Thanks for playing!')



main()