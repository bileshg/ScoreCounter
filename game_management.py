from terminaltables import SingleTable
import player_management as pm
from replit import db


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

    def get_highest_and_lowest_scores(self):
        low_total = self.running_total[0]
        high_total = self.running_total[0]
        for i in range(1, len(self.running_total)):
            total = self.running_total[i]
            if total < low_total:
                low_total = total
            if total > high_total:
                high_total = total

        return low_total, high_total

    def check_winner(self):
        low_total, high_total = self.get_highest_and_lowest_scores()

        if len(self.rounds) == self.max_rounds or high_total >= self.max_score:
            score_to_check = high_total if self.highest_wins else low_total
            winners = []
            for i, total in enumerate(self.running_total):
                if total == score_to_check:
                    winners.append(self.players[i])
            return winners
        else:
            return []

    def end_game(self):
        if len(self.rounds) > 0:
            low_total, high_total = self.get_highest_and_lowest_scores()
            score_to_check = high_total if self.highest_wins else low_total
            winners = []
            for i, total in enumerate(self.running_total):
                if total == score_to_check:
                    winners.append(self.players[i])
            return winners
        else:
            return []
            
    def display(self):
        table = SingleTable(self.data_table, "Scorecard")
        print("\n")
        print(table.table)
        print("\n")


def list_old_games_helper(games):
    print("\n")
    print("[History]".center(24, '-'))
    for i, game in enumerate(games, start=1):
        print(f"{i}. {game.name}")
    print('-' * 24)


def list_old_games():
    games = db.get("history", [])

    if len(games) > 0:
        list_old_games_helper(games)

        try:
            i = int(input("Game to view: ".rjust(22))) - 1
            games[i].display()
        except:
            print("\nPlease provide a valid input!")
    else:
        print("\nNo players added yet!")


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
                    winners = game.check_winner()
                    if len(winners) == 0:                        
                        print("\nThe game goes on...\n")
                    else:                        
                        save_game(game.name, game.data_table, winners)
                        if len(winners) == 1:
                            print("\n" + winners[0] + " was the winner of this game.")
                        elif len(winners) == len(game.players):
                            print("\nWinner undecided...")
                        else:
                            print('\n{}, and {} were the winners of this game.\n'.format(', '.join(winners[:-1]), winners[-1]))
                        choice = 'X'
                        continue
                        
                elif(choice[0] == '2'):
                    game.display()
                
                elif(choice.upper()[0] == 'X'):
                    winners = game.end_game()
                    save_game(game.name, game.data_table, winners)
                    if len(winners) == 0 or len(winners) == len(game.players):                        
                        print("\nWinner Undecided...\n")
                    elif len(winners) == 1:
                        print(winners[0] + " was the winner of this game.")
                    else:
                        print('{}, and {} were the winners of this game.'.format(', '.join(winners[:-1]), winners[-1]))
                
        else:
            print("\nUnable to start a new game!")
        
    else:
        print("\nTwo or more players need to be selected!")


def create_game():
    try:
        print("\n")
        print("[Configure]".center(32, '-'))
        name = input("Name: ")
        highest_wins = input("Who wins? (H - highest scorer, L - Lowest scorer): ")
        max_score = int(input("Maximum score: "))
        max_rounds = int(input("Maximum rounds: "))
        print('-' * 32)
        print("\n")
    except:
        print("\nEnter valid values!")
        return None

    return Game(name, highest_wins.upper()[0] == 'H', max_score, max_rounds)


class History:

    def __init__(self, name, scorecard, winners):
        self.name = name
        self.scorecard = scorecard
        self.winner = winners

    def display(self):
        print("Name: " + self.name)
        table = SingleTable(self.scorecard, "Scorecard")
        print("\n")
        print(table.table)
        print("\n")
        if len(self.winners) == 1:
            print(self.winner + " was the winner of this game.")
        else:
            print('{}, and {} were the winners of this game.'.format(', '.join(self.winners[:-1]), self.winners[-1]))


def save_game(name, scorecard, winners):
    games = db.get("history", [])
    games.append(History(name, scorecard, winners))
    db["history"] = games
