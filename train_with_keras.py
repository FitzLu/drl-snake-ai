import collections
import numpy as np
from agent.brain_keras import KAgent
from env.game import SnakeGame
import matplotlib.pyplot as plt


def main():
    discount_factor = 0.95
    last_frames_num = 4
    actions_num = 3
    exploration_rate = 1.0
    min_exploration_rate = 0.1
    episode_num = 30000
    exploration_decay = ((exploration_rate - min_exploration_rate) / episode_num * 0.5)

    game = SnakeGame(is_tick=False)
    agent = KAgent((last_frames_num,) + game.observation_shape, actions_num)

    for episode in range(episode_num):
        random_count = 0
        predict_count = 0
        loss = 0.0
        w, h = game.observation_shape
        first_step = game.new_round()
        game_over = False        
        
        game.render()
        
        last_frames = collections.deque([first_step.observation] * last_frames_num)
        state = np.array(last_frames)
        state = np.reshape(state, (-1, last_frames_num, w, h))

        while not game_over:
            if np.random.random() < exploration_rate:
                action = np.random.randint(actions_num)
                random_count += 1
                action_type = 'random'
            else:
                action = agent.predict(state)
                predict_count += 1
                action_type = 'predict'

            one_step = game.step(action)

            # print("action_type: %s"%(action_type))

            reward = one_step.reward
            last_frames.append(one_step.observation)
            last_frames.popleft()
            next_state = np.array(last_frames)
            next_state = np.reshape(next_state, (-1, last_frames_num, w, h))
            game_over = one_step.game_over

            agent.store_memory(state, action, reward, next_state, game_over)
            loss += float(agent.learn(discount_factor))

            if game_over is True:
                log = 'episode {:5d} || exploration_rate {:.2f} || random count {:3d} || predict count {:3d}' + \
                        ' || loss {:8.4f} || score {:3d}'
                print(log.format(episode, exploration_rate, random_count, predict_count, loss, game.current_score))
                break

            state = next_state

        if exploration_rate > min_exploration_rate:
            exploration_rate -= exploration_decay

    agent.save_model()

if __name__ == '__main__':
    main()
