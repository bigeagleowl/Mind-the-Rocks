from microbit import *
import random
import radio

ROCKS_ID = 'mtr'
my_id = None
player_num = None
players = []


def start_up_screen():
    """Display the start up screen"""
    display.show(Image.ALL_CLOCKS, delay=100, loop=False, clear=True)
    return


def display_winner():

    print("game over " + str(player_num))
    display.show(Image.SKULL)

    to_finish = len(players) - 1
    print("Remaining players " + str(to_finish))

    if to_finish == 0:
        winner_message = "You are the winner"
        display.scroll(winner_message)
        return

    receivedmess = radio.receive()
    while receivedmess is not None:
        print("Recieved " + receivedmess)
        try:
            (mtrdev, gameover_command, other_id) = receivedmess.split()
        except ValueError:
            receivedmess = radio.receive()
            continue

        if mtrdev == ROCKS_ID and gameover_command == 'GAMEOVER':
            to_finish = to_finish - 1
            print("Already finished - Players remaining >" + str(to_finish))
            if to_finish == 0:
                winner_message = "Winner " + str(player_num)
                print(winner_message)
                display.scroll(winner_message)
                return

        receivedmess = radio.receive()

    while to_finish > 0:
        receivedmess = radio.receive()
        while receivedmess is not None:
            print("Recieved " + receivedmess)
            try:
                (mtrdev, gameover_command, other_id) = receivedmess.split()
            except ValueError:
                receivedmess = radio.receive()
                continue

            if mtrdev == ROCKS_ID and gameover_command == 'GAMEOVER':
                to_finish = to_finish - 1
                print("Awaiting finishing - Players remaining >" +
                      str(to_finish))

                if to_finish == 0:
                    winner_message = "Winner " + str(other_id)
                    print(winner_message)
                    display.scroll(winner_message)
                    return

            receivedmess = radio.receive()


def display_number_of_players(number_of_players):
    """show the number of players found so far on the LEDs"""
    display.clear()
    i = 0
    for y_coord in range(5):
        for x_coord in range(5):
            i += 1
            if i <= number_of_players:
                display.set_pixel(x_coord, y_coord, 9)
            else:
                return


def set_up_multiplayer():
    """connect in multiple players"""

    global player_num
    global my_id
    my_id = random.randint(0, 2147483646)
    global players
    players = []
    players.append(my_id)

    while button_a.is_pressed():

        display_number_of_players(len(players))

        message = ROCKS_ID + " JOINID " + str(my_id)
        print(message)
        radio.send(message)
        sleep(1000)

        receivedmess = radio.receive()
        while receivedmess is not None:
            print("Recieved " + receivedmess)
            try:
                (mtrdev, join_command, other_id) = receivedmess.split()
            except ValueError:
                receivedmess = radio.receive()
                continue

            if mtrdev == ROCKS_ID and join_command == 'JOINID':
                if int(other_id) not in players:
                    players.append(int(other_id))

            receivedmess = radio.receive()

    print(players)

    players.sort()

    print("Sorted list")
    print(players)

    player_num = players.index(my_id) + 1

    print("Player number " + str(player_num))

    random.seed(players[0])

    display.scroll(str(player_num), monospace=True, delay=1000)
    button_a.get_presses()
    button_b.get_presses()


# rock generator same for playe
def more_rocks():
    for x_coord in range(5):
        rock = random.randint(0, 10)
        if rock == 0:
            display.set_pixel(x_coord, 0, 9)
        else:
            display.set_pixel(x_coord, 0, 0)


# rock roller
def move_rocks_down():

    for y_coord in reversed(range(4)):
        for x_coord in range(5):
            display.set_pixel(x_coord, y_coord + 1,
                              display.get_pixel(x_coord, y_coord))


def main():
    """Main function for the Mind the Rocks"""
    multiple_player = False
    multiple_player_games_played = 0 
    delay = 1000
    games_played =0
    
    radio.on()

    start_up_screen()

    if button_a.is_pressed():
        set_up_multiplayer()
        multiple_player = True

    x_coord_ship = 2
    display.set_pixel(x_coord_ship, 4, 9)

    while True:
        # move rocks
        move_rocks_down()

        if display.get_pixel(x_coord_ship, 4):
            print("find winner my_id is " + str(player_num))
            if multiple_player:
                message = ROCKS_ID + " GAMEOVER " + str(player_num)
                print(message)
                radio.send(message)

            # display.scroll("Game Over")

            if multiple_player:
                display_winner()
            if button_a.is_pressed():
                set_up_multiplayer()

            multiple_player_games_played += 1
            random.seed(players[0] + multiple_player_games_played)

            start_up_screen()
            x_coord_ship = 2
            delay = 1000

        # display ship
        display.set_pixel(x_coord_ship, 4, 9)

        more_rocks()

        sleep(delay)
        if delay > 100:
            delay = delay - 2
        message = "Delay>" + str(delay) + "ms"
        print(message)

        x_coord_ship = x_coord_ship - button_a.get_presses() + \
            button_b.get_presses()
        if x_coord_ship > 4:
            x_coord_ship = 4
        elif x_coord_ship < 0:
            x_coord_ship = 0


if __name__ == "__main__":
    main()
