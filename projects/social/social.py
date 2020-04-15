import random

class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, user):
        self.queue.append(user)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        for user in range(num_users):
            self.add_user(user)

        # create a list with all possible friend connections
        friendships = []
        for user in range(1, self.last_id + 1):
            for friend in range(user + 1, num_users + 1):
                friendships.append((user, friend))

        # shuffle the list
        random.shuffle(friendships)

        # grab first N elements of list
        total_friendships = num_users * avg_friendships
        pairs_needed = total_friendships // 2
        random_friendships = friendships[:pairs_needed]

        # Create friendships
        for friendship in random_friendships:
            print(friendship)
            self.add_friendship(friendship[0], friendship[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set

        # BFS
        # queue
        q = Queue()
        path = [user_id]

        # current path starting with user_id
        q.enqueue(path)

        # iter through friendships



        # while q.size() > 0:
        #     ## dequeue and capture start user
        #     cur_path = q.dequeue()
        #     cur_user = cur_path[-1]

        #     ## node check
        #     if cur_user == user_id:
        #         ### return if user_id match
        #         return cur_path

        #     ### for each friendship
        #     for friendship in self.friendships:
        #         print(friendship)
        #         ## visited check
        #         if cur_user not in visited or visited[cur_user][friendship]:
        #             ### add user is visited
        #             visited[cur_user].append[friendship]

        #         #### create path copy
        #         path_copy = cur_path[:]
        #         #### queue path copy with user of friendship
        #         path_copy.append(friendship)
        #         q.enqueue(path_copy)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships, '\n\n')
    connections = sg.get_all_social_paths(1)
    print('connex', connections)
