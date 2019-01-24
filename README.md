# Deep reinforcement learning snake ai
This program uses deep reinforcement learning to train Snakes.We constructed a 10x10 pixel matrix with a red pixel representing the apple and blue pixel representing the snake. At the beginning, we let the snake do some random exploration, try to eat apples step by step, each frame of the game represents a state of the current game. We take the continuous four frames as the experience input into the neural network, whether to eat apples at each step, whether to survive, whether the game ends as a feedback of each action to reversely stimulate neural network learning. Also, we add random slices from past memories to the current training to prevent overfitting.

## Neural Networks
| Layer (type)              | Output Shape     | Param  |
|---------------------------|------------------|--------|
| conv2d_1 (Conv2D)         | (None, 16, 8, 8) | 592    |
| activation_1 (Activation) | (None, 16, 8, 8) | 0      |
| conv2d_2 (Conv2D)         | (None, 32, 6, 6) | 4640   |
| activation_2 (Activation) | (None, 32, 6, 6) | 0      |
| flatten_1 (Flatten)       | (None, 1152)     | 0      |
| dense_1 (Dense)           | (None, 256)      | 295168 |
| activation_3 (Activation) | (None, 256)      | 0      |
| dense_2 (Dense)           | (None, 3)        | 771    |


## Run
```
python train_with_keras.py
```

## Dependencies
- Python 3.6
- Tensorflow 1.1
- Keras
- Pygame