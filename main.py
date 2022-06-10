import player_management as pm
import game_management as gm


def main():
    choice = '0'
    while choice.upper()[0] != 'X':
        print("[Menu]".center(24, '-'))
        print("1. Start a new game")
        print("2. Add Player")
        print("3. List Players")
        print("4. Remove Player")
        print("5. History")
        print("X. Exit")
        print('-' * 24)

        choice = input("Your choice: ".rjust(22))

        if(choice[0] == '1'):
            gm.start_game()
        elif(choice[0] == '2'):
            pm.add_player()
        elif(choice[0] == '3'):
            pm.list_players()
        elif(choice[0] == '4'):
            pm.remove_player()
        elif(choice[0] == '5'):
            gm.list_old_games()
        elif(choice.upper()[0] == 'X'):
            print("\nBye!")
        else:
            print("\nPlease provide a valid input!")

        print("\n")


if __name__ == "__main__":
    main()
