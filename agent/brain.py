import tensorflow as tf
import numpy as np
from agent.memory import Memory

class Agent(object):

    def __init__(self,
                 last_frames_num,
                 observation_shape,
                 actions_num,
                 channels):
        self.last_frames_num = last_frames_num
        self.observation_shape = observation_shape
        self.channels = channels
        self.features_shape = (last_frames_num,) + observation_shape
        self.memory = Memory(self.features_shape, actions_num, 1000)
        self.build_layers(last_frames_num, actions_num, observation_shape)

    def build_layers(self, last_frames_num, actions, observation_shape):
        w, h = observation_shape
        self.states = tf.placeholder(tf.float32, [None, last_frames_num, w, h])
        self.actions = tf.placeholder(tf.int32, [None, ])
        self.rewards = tf.placeholder(tf.float32, [None, ])
        self.states_next = tf.placeholder(tf.float32, [None, last_frames_num, w, h])

        with tf.variable_scope('q'):
            w, h = observation_shape
            conv1 = tf.layers.conv2d(
                inputs=self.states,
                filters=16,
                kernel_size=(3,3),
                strides=(1, 1),
                padding='same',
                data_format='channels_first',
                activation=tf.nn.relu
            )

            w = w - 3 + 2
            h = h - 3 + 2

            conv2 = tf.layers.conv2d(
                inputs=conv1,
                filters=32,
                kernel_size=(3,3),
                strides=(1, 1),
                padding='same',
                data_format='channels_first',
                activation=tf.nn.relu
            )

            w = w - 3 + 2
            h = h - 3 + 2

            conv2_flat = tf.reshape(conv2, [-1, 12800])
            dense = tf.layers.dense(inputs=conv2_flat, units=256, activation=tf.nn.relu,
                                    kernel_initializer=tf.random_normal_initializer(0, 0.1))
            self.q = tf.layers.dense(inputs=dense, units=actions,
                                     kernel_initializer=tf.random_normal_initializer(0, 0.1))

        GAMMA = 0.9
        q_target = self.rewards + GAMMA * tf.reduce_max(self.q, axis=1)
        one_hot = tf.one_hot(self.actions, depth=actions, dtype=tf.float32)
        q_current = tf.reduce_sum(self.q * one_hot, axis=1)

        loss = tf.reduce_mean(tf.squared_difference(q_target, q_current))
        self.train_op = tf.train.AdamOptimizer(0.8).minimize(loss)

        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    def store_memory(self, state, action, reward, state_next):
        self.memory.store(state, action, reward, state_next)

    def learn(self):
        states, actions, rewards, states_next = self.memory.get_batch(50)
        self.sess.run(self.train_op, {self.states: states, self.actions: actions,
                                 self.rewards: rewards, self.states_next: states_next})


    def predict(self, state):
        actions_value = self.sess.run(self.q, feed_dict={self.states: state})
        action = np.argmax(actions_value)
        return action