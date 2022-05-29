from model import Model
import gym
from pogema.animation import AnimationMonitor
from pogema import GridConfig

def main():
    _size = 20
    _num_agents = 10
    _density = 0.2
    # Define random configuration
    grid_config = GridConfig(num_agents=_num_agents,  # количество агентов на карте
                             size=_size,  # размеры карты
                             density=_density,  # плотность препятствий
                             seed=1,  # сид генерации задания
                             max_episode_steps=1024,  # максимальная длина эпизода
                             obs_radius=5,  # радиус обзора
                             )

    env = gym.make("Pogema-v0", grid_config=grid_config)
    env = AnimationMonitor(env)

    # обновляем окружение
    obs = env.reset()

    done = [False for k in range(len(obs))]
    solver = Model()
    steps = 0
    while not all(done):
        # Используем AStar
        varToPrint = solver.act(obs, done,
            env.get_agents_xy_relative(),
            env.get_targets_xy_relative())
        obs, reward, done, info = env.step(varToPrint)
        steps += 1
        print(steps, varToPrint)

    # сохраняем анимацию и рисуем ее
    env.save_animation(f"render/render_{_size}_{_num_agents}_{_density}.svg", egocentric_idx=None)


if __name__ == '__main__':
    main()
