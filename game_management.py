import os.path
import pickle
from terminaltables import SingleTable
import player_management as pm


HISTORY_FILE = 'history.pkl'


class Game:

    def __init__(self, name, highest_wins, max_score, max_rounds):
        self.name = name
        self.highest_wins = highest_wins
        self.max_score = max_score
        self.max_rounds = max_rounds

    def start_game(self, players):
        self.players = players
        self.running_total = [0] * len(players)
        self.rounds = []
        self.data_table = [
            ["Players:"] + self.players,
            ["Total:"] + self.running_total
        ]

    def add_round(self):
        try:
            print("\n")
            
            scores = []
            for player in self.players:
                score = int(input(f"{player}'s score: "))
                scores.append(score)

            for i, score in enumerate(scores):
                self.running_total[i] += score

            self.rounds.append(scores)
            
            self.data_table = [
                ["Players:"] + self.players
            ]

            for i, round in enumerate(self.rounds, start=1):
                self.data_table.append([i] + round)

            self.data_table.append(["Total:"] + self.running_total)
        except:
            print("\nEnter valid scores!")

    def get_highest_and_lowest_scorer(self):
        low_total = self.running_total[0]
        low_index = 0        
        high_total = self.running_total[0]
        high_index = 0
        for i in range(1, len(self.running_total)):
            total = self.running_total[i]
            if total < low_total:
                low_total = total
                low_index = i
            if total > high_total:
                high_total = total
                high_index = i

        return low_total, low_index, high_total, high_index

    def check_winner(self):
        low_total, low_index, high_total, high_index = self.get_highest_and_lowest_scorer()

        if len(self.rounds) == self.max_rounds or high_total >= self.max_score:
            if self.highest_wins:
                return self.players[high_index]
            else:
                return self.players[low_index]
        else:
            return None

    def end_game(self):
        if len(self.rounds) > 0:
            low_total, low_index, high_total, high_index = self.get_highest_and_lowest_scorer()
    
            if self.highest_wins:
                return self.players[high_index]
            else:
                return self.players[low_index]
        else:
            return None
            
    def display(self):
        table = SingleTable(self.data_table, "Scorecard")
        print("\n")
        print(table.table)
        print("\n")


def get_old_games():
    if os.path.exists(HISTORY_FILE):
        file = open(HISTORY_FILE, 'rb')
        games = pickle.load(file)
        file.close()

        return games
    else:
        return []


def start_game():
    selected_players = pm.select_players()

    if len(selected_players) > 1:        
        game = create_game()
        
        if game is not None:
            game.start_game(selected_players)
            
            choice = '0'
            while choice.upper()[0] != 'X':
                print("[Game]".center(24, '-'))
                print("1. New Round")
                print("2. Scoreboard")
                print("X. End Game")
                print('-' * 24)
        
                choice = input("Your choice: ".rjust(22))
        
                if(choice[0] == '1'):
                    game.add_round()
                    winner = game.check_winner()
                    if winner is not None:
                        print(f"{winner} is the winner!\n")
                        choice = 'X'
                        continue
                    else:
                        print("\nThe game goes on...\n")
                elif(choice[0] == '2'):
                    game.display()
                elif(choice.upper()[0] == 'X'):
                    winner = game.end_game()
                    if winner is not None:
                        print(f"{winner} is the winner!")
                    else:
                        print("\nWinner undecided...")                
                
        else:
            print("\nUnable to start a new game!")
        
    else:
        print("\nTwo or more players need to be selected!")


def create_game():
    try:
        print("\n")
        print("[Configure]".center(32, '-'))
        name = input("Name: ")
        highest_wins = input("Highest score wins? (y/n): ")
        max_score = int(input("Maximum score: "))
        max_rounds = int(input("Maximum rounds: "))
        print('-' * 32)
        print("\n")
    except:
        print("\nEnter valid values!")
        return None

    return Game(name, highest_wins.upper()[0] == 'Y', max_score, max_rounds)
