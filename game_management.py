from terminaltables import SingleTable
import player_management as pm
from replit import db
import uuid
import json


class Game:
    def __init__(self, name, highest_wins, max_score, max_rounds):
        self.data_table = None
        self.rounds = None
        self.running_total = None
        self.players = None
        self.name = name
        self.highest_wins = highest_wins
        self.max_score = max_score
        self.max_rounds = max_rounds

    def start_game(self, players):
        self.players = players
        self.running_total = [0] * len(players)
        self.rounds = []
        self.data_table = [["Players:"] + self.players,
                           ["Total:"] + self.running_total]

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

            self.data_table = [["Players:"] + self.players]

            self.data_table.extend(
                [i] + round for i, round in enumerate(self.rounds, start=1)
            )
            self.data_table.append(["Total:"] + self.running_total)
        except Exception:
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
            return [
                self.players[i]
                for i, total in enumerate(self.running_total)
                if total == score_to_check
            ]
        else:
            return []

    def end_game(self):
        if len(self.rounds) <= 0:
            return []
        low_total, high_total = self.get_highest_and_lowest_scores()
        score_to_check = high_total if self.highest_wins else low_total
        return [
            self.players[i]
            for i, total in enumerate(self.running_total)
            if total == score_to_check
        ]

    def display(self):
        table = SingleTable(self.data_table, "Scorecard")
        print("\n")
        print(table.table)
        print("\n")


def list_old_games_helper(games):
    print("\n")
    print("[History]".center(24, '-'))
    for i, game_id in enumerate(games, start=1):
        game_json = json.loads(db[game_id])
        print(f"{i}. {game_json['name']}")
    print('-' * 24)


def list_old_games():
    games = db.prefix("GM-")

    if len(games) > 0:
        list_old_games_helper(games)

        try:
            i = int(input("Game to view: ".rjust(22))) - 1
            display_old_game(db[games[i]])
        except Exception:
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

                if choice[0] == '1':
                    game.add_round()
                    winners = game.check_winner()
                    if len(winners) == 0:
                        print("\nThe game goes on...\n")
                    else:
                        save_game(game.name, game.data_table, winners)
                        if len(winners) == 1:
                            print("\n" + winners[0] +
                                  " was the winner of this game.")
                        elif len(winners) == len(game.players):
                            print("\nWinner undecided...")
                        else:
                            print(
                                f"\n{', '.join(winners[:-1])}, and {winners[-1]} were the winners of this game.\n"
                            )
                        choice = 'X'
                        continue

                elif choice[0] == '2':
                    game.display()

                elif choice.upper()[0] == 'X':
                    winners = game.end_game()
                    save_game(game.name, game.data_table, winners)
                    if len(winners) in [0, len(game.players)]:
                        print("\nWinner Undecided...\n")
                    elif len(winners) == 1:
                        print(f"{winners[0]} was the winner of this game.")
                    else:
                        print(
                            f"{', '.join(winners[:-1])}, and {winners[-1]} were the winners of this game."
                        )

        else:
            print("\nUnable to start a new game!")

    else:
        print("\nTwo or more players need to be selected!")


def create_game():
    try:
        print("\n")
        print("[Configure]".center(32, '-'))
        name = input("Name: ")
        highest_wins = input(
            "Who wins? (H - highest scorer, L - Lowest scorer): ")
        max_score = int(input("Maximum score: "))
        max_rounds = int(input("Maximum rounds: "))
        print('-' * 32)
        print("\n")
    except Exception:
        print("\nEnter valid values!")
        return None

    return Game(name, highest_wins.upper()[0] == 'H', max_score, max_rounds)


def display_old_game(game_json_string):
    game = json.loads(game_json_string)
    print("Name: " + game['name'])
    table = SingleTable(game['scorecard'], "Scorecard")
    print("\n")
    print(table.table)
    print("\n")
    if len(game['winners']) == 1:
        print(game['winners'][0] + " was the winner of this game.")
    else:
        print(
            f"{', '.join(game['winners'][:-1])}, and {game['winners'][-1]} were the winners of this game."
        )


def save_game(name, scorecard, winners):
    game_to_save = {"name": name, "scorecard": scorecard, "winners": winners}
    db[f'GM-{uuid.uuid1()}'] = json.dumps(game_to_save)


def demo_game():
    print('-' * 35)
    print("""
    
░█▀▄░█▀▀░█▄█░█▀█░░░█▄█░█▀█░█▀▄░█▀▀
░█░█░█▀▀░█░█░█░█░░░█░█░█░█░█░█░█▀▀
░▀▀░░▀▀▀░▀░▀░▀▀▀░░░▀░▀░▀▀▀░▀▀░░▀▀▀

Please fork this Repl and  set the 
DEMO_MODE flag in main.py to False
to test it out with DB.

The DB does not instantiate if you 
directly run it.
    
    """)
    print('-' * 35)

    no_of_players = int(input("\n# of players: ").strip())

    if no_of_players > 1:

        selected_players = []
        for i in range(no_of_players):
            name = input(f"\nName of player #{i+1}: ")
            selected_players.append(name)

        game = create_game()

        if game is not None:
            game.start_game(selected_players)

            choice = '0'
            while True:
                print("[Game]".center(24, '-'))
                print("1. New Round")
                print("2. Scoreboard")
                print("X. End Game")
                print('-' * 24)

                choice = input("Your choice: ".rjust(22))

                if choice[0] == '1':
                    game.add_round()
                    winners = game.check_winner()
                    if len(winners) == 0:
                        print("\nThe game goes on...\n")
                    else:
                        if len(winners) == 1:
                            print("\n" + winners[0] +
                                  " was the winner of this game.")
                        elif len(winners) == len(game.players):
                            print("\nWinner undecided...")
                        else:
                            print(
                                f"\n{', '.join(winners[:-1])}, and {winners[-1]} were the winners of this game.\n"
                            )
                        break

                elif choice[0] == '2':
                    game.display()

                elif choice.upper()[0] == 'X':
                    winners = game.end_game()
                    if len(winners) in [0, len(game.players)]:
                        print("\nWinner Undecided...\n")
                    elif len(winners) == 1:
                        print(f"{winners[0]} was the winner of this game.")
                    else:
                        print(
                            f"{', '.join(winners[:-1])}, and {winners[-1]} were the winners of this game."
                        )
                    break

        else:
            print("\nUnable to start a new game!")

    else:
        print("\nAt least two players needed!")
    
