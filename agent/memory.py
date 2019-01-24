import numpy as np
import collections
import random

class Memory(object):

    def __init__(self, input_shape, num_actions, memory_size=100):
        self.memory = collections.deque() #双向队列
        self.input_shape = input_shape
        self.num_actions = num_actions
        self.memory_size = memory_size
    
    def reset(self):
        self.memory = collections.deque()

    def store(self, state, action, reward, next_state, is_end):
        s = state.flatten()
        a = np.array(action).flatten()
        r = np.array(reward).flatten()
        s_ = next_state.flatten()
        end = 1 * np.array(is_end).flatten()
        experience = np.concatenate([s, a, r, s_, end])
        self.memory.append(experience)
        if 0 < self.memory_size < len(self.memory):
            self.memory.popleft()

    def get_batch(self, batch_size):
        batch_size = min(len(self.memory), batch_size)
        experience = np.array(random.sample(self.memory, batch_size))
        input_dim = np.prod(self.input_shape) # shape 相乘

        states = experience[:, 0:input_dim]
        actions = experience[:, input_dim]
        rewards = experience[:, input_dim+1]
        next_state = experience[:, input_dim + 2 : input_dim * 2 + 2]
        ends = experience[:, input_dim * 2 + 2]

        states = states.reshape((batch_size, ) + self.input_shape)
        next_state = next_state.reshape((batch_size, ) + self.input_shape)

        return states, actions, rewards, next_state, ends, batch_size