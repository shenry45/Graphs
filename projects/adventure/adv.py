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
room_graph=literal_eval(open(map_file[1], "r").read())
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

#DFT
visited = []
s = Stack()
path = [player.current_room.id]
s.push(path)

while s.size() > 0:
    ## pop off top of stack, the current_room
    current_path = s.pop()
    current_room = current_path[-1]
    print('**cur room', current_room)

    if current_room not in traversal_graph:
        traversal_graph[current_room] = {'n': '?', 'e': '?', 's': '?', 'w': '?'}

        ### get possible directions
        dirs = world.rooms[current_room].get_exits()

        # Mark invalid directions as None
        compass = ['n', 'e', 's', 'w']
        for direction in compass:
            if direction not in dirs:
                traversal_graph[current_room][direction] = 'None'

        # iter through moveable directions
        for direction in dirs:
            possible = world.rooms[current_room].get_room_in_direction(direction)
            print(possible.id)

            if possible is None or possible.id in traversal_graph:
                continue

            path_copy = current_path[:]
            print(current_path, type(current_path))
            path_copy.append(possible.id)
            # add to graph
            traversal_graph[current_room][direction] = possible.id
            # add direction to players traveled path
            # traversal_path.append(direction)
            # push onto DFT stack
            s.push(path_copy)
    else:
        break

print(traversal_path)
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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
