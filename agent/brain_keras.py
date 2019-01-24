import keras
from keras.models import Sequential
from keras.layers import *
from keras.optimizers import *
from agent.memory import Memory


class KAgent(object):
    def __init__(self, features_shape, actions):
        self.actions = actions
        self.memory = Memory(features_shape, actions, 1000)
        from keras.models import load_model
        self.model = self.build_layers(features_shape, actions)

    def build_layers(self, features_shape, actions):
        model = Sequential()
        model.add(Conv2D(
            16,
            kernel_size=(3, 3),
            strides=(1, 1),
            data_format='channels_first',
            input_shape=features_shape))

        model.add(Activation('relu'))
        model.add(Conv2D(
            32,
            kernel_size=(3, 3),
            strides=(1, 1),
            data_format='channels_first'))
        model.add(Activation('relu'))
        model.add(Flatten())
        model.add(Dense(256))
        model.add(Activation('relu'))
        model.add(Dense(actions))
        
        model.compile(optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True), loss='MSE')

        callback = keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=50, write_graph=True, write_grads=False, 
        write_images=False, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None)

        callback.set_model(model)

        model.summary()

        return model

    def store_memory(self, state, action, reward, state_next, game_is_over):
        self.memory.store(state, action, reward, state_next, game_is_over)

    def learn(self, discount_factor):
        states, actions, rewards, states_next, is_ends, size = self.memory.get_batch(50)
        actions = np.cast['int'](actions)
        rewards = rewards.repeat(self.actions).reshape((size, self.actions))
        is_ends = is_ends.repeat(self.actions).reshape((size, self.actions))

        X = np.concatenate([states, states_next], axis=0)
        y = self.model.predict(X)
        Q_next = np.max(y[size:], axis=1).repeat(self.actions).reshape((size, self.actions))

        delta = np.zeros((size, self.actions))
        delta[np.arange(size), actions] = 1

        targets = (1 - delta) * y[:size] + delta * (rewards + discount_factor * (1 - is_ends) * Q_next)  
        loss = self.model.train_on_batch(states, targets)

        return loss

    def predict(self, states):
        q = self.model.predict(states)[0]
        return np.argmax(q)

    def save_model(self):
        self.model.save('agent-keras-final.model')
