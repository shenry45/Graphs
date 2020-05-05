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
room_graph=literal_eval(open(map_file[0], "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = []

traversal_graph = {}

class Queue:
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            last = self.queue[0]
            self.queue.pop(0)
            return last
        else:
            return None
    def size(self):
        return len(self.queue)

possible_dirs = {}
current_dirs = player.current_room.get_exits()
reverse_dir = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

for exit in current_dirs:
    possible_dirs[exit] = '?'
    traversal_graph[player.current_room.id] = possible_dirs 

def find_next_route(node):
    visited = []
    q = Queue()
    q.enqueue([node])

    while q.size() > 0:
        path = q.dequeue()
        cur_room = path[-1]

        if cur_room not in visited:
            for dir in traversal_graph[cur_room]:
                if traversal_graph[cur_room][dir] == '?':
                    return path
            visited.append(cur_room)
            for und_dir in traversal_graph[cur_room]:
                path_copy = path[:]
                path_copy.append(traversal_graph[cur_room][und_dir])
                q.enqueue(path_copy)
        
    return []

def pathDirections(path):
    directions = []
    cur_room = path[0]
    path = path[1:]
    for room in path:
        for exit in traversal_graph[cur_room]:
            if room == traversal_graph[cur_room][exit]:
                directions.append(exit)
    return directions

while True:
    cur_room_exits = traversal_graph[player.current_room.id]
    move_dirs = []

    # if exit not discovered, add to directions to move
    for dir in cur_room_exits:
        if cur_room_exits[dir] == '?':
            move_dirs.append(dir)

    if len(move_dirs) > 0:
        direction = move_dirs[0]
        # move player
        traversal_path.append(direction)
        last_room = player.current_room.id
        player.travel(direction)
        possible_dirs = {}

        # now if new room not in graph
        if player.current_room.id not in traversal_graph:
            for exit in player.current_room.get_exits():
                possible_dirs[exit] = '?'
            traversal_graph[player.current_room.id] = possible_dirs
        # set to and from path for recent rooms
        traversal_graph[last_room][direction] = player.current_room.id
        traversal_graph[player.current_room.id][reverse_dir[direction]] = last_room
    else:
        # find closest not discovered room
        walkDirections = find_next_route(player.current_room.id)
        if len(walkDirections) == 0:
            break
        for direction in pathDirections(walkDirections):
            player.travel(direction)
            traversal_path.append(direction)



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
