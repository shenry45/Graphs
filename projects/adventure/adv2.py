from room import Room
from player import Player
from world import World
from pathlib import Path

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_folder = Path(f"{Path.cwd()}/maps/")
map_file = [
    map_folder / "main_maze.txt",
    map_folder / "test_cross.txt",
    map_folder / "test_line.txt",
    map_folder / "test_loop_fork.txt",
    map_folder / "test_loop.txt"
]

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file[2], "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = []

traversal_graph = {}

class Stack:
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Queue:
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size > 0:
            last = self.queue[0]
            self.queue.pop(0)
            return last
        else:
            return None
    def size(self):
        return len(self.queue)

path = [player.current_room]

# while len(traversal_graph) < 500:
# if player's room not searched
if player.current_room.id not in traversal_graph:
    # add room to graph
    traversal_graph[player.current_room.id] = {'n': '?', 'e': '?', 's': '?', 'w': '?'}

# get all possible directions
for direction in traversal_graph[player.current_room.id].keys():
    print(direction)
    possible = player.current_room.get_room_in_direction(direction)
    print(possible)

    if possible is None:
        traversal_graph[player.current_room.id][direction] = None
    else:
        traversal_path.append(direction)
        traversal_graph[player.current_room.id][direction] = player.travel(direction)


print(traversal_graph)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
