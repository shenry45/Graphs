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
room_graph=literal_eval(open(map_file[3], "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = []

traversal_graph = {}
# fill traversal graph to match room count
for numb in range(len(room_graph)):
    traversal_graph[numb] = {'n': '?', 'e': '?', 's': '?', 'w': '?'}

class Stack:
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size > 0:
            last = self.stack[-1]
            self.stack.pop(self.size-1)
            return last
        else:
            return None
    def size(self):
        return len(self.stack)

#DFS
visited = []
s = Stack()
path = [player.current_room.id]
s.push(path)
# create pointer for fork
fork = 0

while s.size > 0:
    # get current room
    current_room = s.pop()
    # create current path
    current_path = [current_room]

    # find all directions possible
    dirs = room_graph[current_room.id][1]

    # if multiple directions from current possible
    # if len(dirs) > 1:
        # update fork and current path


    # loop through directions possible
    for direction in dirs:
        # create path copy
        path_copy = current_path[:]

        # current node visited and same as pointer?
        if room_graph[current_room][direction] is visited and current_room == fork:
            print('fork found')
            # append to current path
            # break loop

        # current node visited?
        if current_room in visited:
            # append current path to traversal_path

        # else not visited
            # change 
            # add 
    
    s.pop()



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
