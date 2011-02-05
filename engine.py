import copy

from ant_map import *
from random_bot import *
from hunter_bot import *

player_count = 4

def switch_players(m, a, b):
    m = m.clone()
    for x in range(m.width):
        for y in range(m.height):
            if m.map[x][y] == a:
                m.map[x][y] = b
            elif m.map[x][y] == b:
                m.map[x][y] = a
    return m

def save_image(map, turn, anno=""):
    img = map.render()
    scale = 4
    new_size = (img.size[0] * scale, img.size[1] * scale)
    img = img.resize(new_size)
    img.save("playback/frame" + str(turn).zfill(5) + anno + ".png")

def play_game(map_filename):
    m = AntMap(map_filename)
    players = [HunterBot() for i in range(m.num_players)]
    initial_food_density = 0.01
    food_amount = int(initial_food_density * m.land_area)
    m.do_food(food_amount)
    turn_count = 1
    while not m.game_over() and turn_count < 400:
        print "turn:", turn_count
        #save_image(m, turn_count, 'start')
        for i, player in enumerate(players):
            player_number = i + 1
            reflected_map = switch_players(m, player_number, 1)
            orders = player.do_turn(reflected_map)
            m.do_orders(player_number, orders)
            #for order in orders:
            #    m.do_order(i, order)
            # save_image(m, turn_count, 'player' + str(i+1))
        m.resolve_orders()
        #save_image(m, turn_count, 'move')
        #m.do_turn()
        m.do_death()
        #save_image(m, turn_count, 'death')
        m.do_birth()
        #save_image(m, turn_count, 'birth')
        m.do_food()
        #save_image(m, turn_count, 'food')
        turn_count += 1
    #save_image(m, turn_count, 'start')

random.seed(0)
import cProfile
cProfile.run('play_game("simple2.txt")')
