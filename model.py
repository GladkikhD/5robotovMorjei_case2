
import random
import gym
from pogema.wrappers.multi_time_limit import MultiTimeLimit
from pogema.animation import AnimationMonitor
from IPython.display import SVG, display
import numpy as np
import pogema
from pogema import GridConfig
import _5robotovMorjei

class Model:
    def __init__(self):
        pass

    def act(self, obs, dones, positions_xy, targets_xy) -> list:
        net = _5robotovMorjei.Net()
        results = list[int]()
        for i in range(len(obs)):
            if positions_xy[i] == targets_xy[i]:
                results.append(0)
                continue
            results.append(net.findWay(positions_xy[i], targets_xy))
        print(results)
        return results

        #results = [random.randint(0,4) for _ in range(len(obs))]


def main():
    # Define random configuration
    grid_config = GridConfig(num_agents=5, # количество агентов на карте
                            size=8,      # размеры карты
                            density=0.3,  # плотность препятствий
                            seed=1,       # сид генерации задания 
                            max_episode_steps=256,  # максимальная длина эпизода
                            obs_radius=5, # радиус обзора
                            )

    env = gym.make("Pogema-v0", grid_config=grid_config)
    env = AnimationMonitor(env)

    # обновляем окружение
    obs = env.reset()

    print(obs)

    done = [False, ...]

    model = Model()

    while not all(done):
        # Используем act
        obs, reward, done, info = env.step(model.act(
            obs, done, env.get_agents_xy_relative(), env.get_targets_xy_relative()))

    # сохраняем анимацию и рисуем ее
    env.save_animation("render.svg", egocentric_idx=0)
    display(SVG('render.svg'))

    #0 - на месте, 1 - вверх, 2 - вниз, 3 - влево, 4 - вправо
main()
