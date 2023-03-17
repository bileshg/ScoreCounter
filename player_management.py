from replit import db


def add_player():
    players = db.get("players", [])

    name = input("\nEnter player's name: ")
    players.append(name)

    db["players"] = players


def list_players_helper(players):
    print("\n")
    print("[Players]".center(24, '-'))
    for i, player in enumerate(players, start=1):
        print(f"{i}. {player}")
    print('-' * 24)


def list_players():
    players = db.get("players", [])

    if len(players) > 0:
        list_players_helper(players)
    else:
        print("\nNo players added yet!")


def remove_player():
    players = db.get("players", [])

    if len(players) > 0:
        list_players_helper(players)

        try:
            i = int(input("Player # to remove: ".rjust(22))) - 1
            players.remove(players[i])

            db["players"] = players
        except:
            print("\nPlease provide a valid input!")
    else:
        print("\nNo players added yet!")


def select_players():
    players = db.get("players", [])

    selected_players = []

    if len(players) > 0:
        list_players_helper(players)

        try:
            n = int(input("# of players: ".rjust(22)))

            if (len(players) < n):
                print(f"Only {len(players)} added!")
                return []

            print("\n")
            for i in range(1, n + 1):
                j = int(input(f"Player #{i}: ")) - 1
                player = players[j]
                if player not in selected_players:
                    selected_players.append(player)
                else:
                    print("\nPlayer already selected!")
                    i = -1
        except:
            print("\nPlease provide a valid input!")
            return []
    else:
        print("\nNo players added yet!")

    return selected_players
