import collections
import numpy as np
from env.game import SnakeGame
from agent.brain import Agent


def main():
    last_frames_num = 4
    actions_num = 3
    exploration_rate = 1.0
    min_exploration_rate = 0.1
    episode_num = 10000
    exploration_decay = ((exploration_rate - min_exploration_rate) / episode_num)

    game = SnakeGame(is_tick=True)
    agent = Agent(last_frames_num, game.observation_shape, actions_num, 0)

    for episode in range(episode_num):
        first_step = game.new_round()
        game.render()
        game_over = False

        w, h = game.observation_shape

        last_frames = collections.deque([first_step.observation] * last_frames_num)
        state = np.array(last_frames)
        state = np.reshape(state, (-1, last_frames_num, w, h))

        while not game_over:
            if np.random.random() < exploration_rate:
                action = np.random.randint(actions_num)
            else:
                action = agent.predict(state)

            one_step = game.step(action)

            reward = one_step.reward
            last_frames.append(one_step.observation)
            last_frames.popleft()
            next_state = np.array(last_frames)
            next_state = np.reshape(next_state, (-1, last_frames_num, w, h))
            game_over = one_step.game_over

            agent.store_memory(state, action, reward, next_state)
            agent.learn()

            if game_over is True:
                break

            state = next_state
            if exploration_rate > min_exploration_rate:
                exploration_rate -= exploration_decay


if __name__ == '__main__':
    main()
