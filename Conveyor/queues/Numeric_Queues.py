# Numeric Queue Class

from collections import deque


class Numeric_Queues(object):
    def __init__(self, name):
        self.queues = {}
        self.queues[name] = deque()
        self.current_queue = name

    # functionality for @ operator
    def at(self, id):
        if not id in self.queues.keys():
            self.queues[id] = deque()
        self.current_queue = id

    def append(self, val):
        self.queues[self.current_queue].append(val)

    def popleft(self):
        return self.queues[self.current_queue].popleft()

    # overload len
    def __len__(self):
        return len(self.queues[self.current_queue])

    # overload []
    def __getitem__(self, key):
        return self.queues[self.current_queue][key]

    def clear(self):
        self.queues[self.current_queue].clear()
