'''
Replay buffer for storing RL experiences.
'''

import random

class ReplayBuffer:

    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        self.buffer = []
        self.position = 0

    def push(self, experience):

        if len(self.buffer) < self.capacity:
            self.buffer.append(None)

        self.buffer[self.position] = experience
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size: int):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)