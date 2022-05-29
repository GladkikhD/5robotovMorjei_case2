from asyncio.windows_events import NULL
from collections import deque
from msilib import sequence
from typing import Tuple
import numpy as np
from heapq import heappop, heappush
import gym
from pogema.animation import AnimationMonitor
from pogema import GridConfig


class Node:
    def __init__(self, coord: Tuple[int, int] = (0, 0), g: int = 0, h: int = 0):
        self.i, self.j = coord
                                           #AStar algorithm
        self.g = g                         #наименьшая стоимость пути в v из стартовой вершины
        self.h = h                         #эвристическое приближение стоимости пути от v до конечной цели.
        self.f = g + h                     #длина пути до цели, которая складывается из пройденного расстояния g(v) и оставшегося расстояния h(v).

    def __lt__(self, other):
        return self.f < other.f or ((self.f == other.f) and (self.g < other.g))


class AStar:
    def __init__(self):
        self.start = (0, 0) 
        self.goal = (0, 0)
        self.max_steps = 10000  #максимальное число шагов для алгоритма
        self.OPEN = list()
        self.CLOSED = dict()
        self.obstacles = set()
        self.other_agents = set()

    def best_way(self, start, goal):
        self.start = start
        self.goal = goal
        self.CLOSED = dict()
        self.OPEN = list()
        heappush(self.OPEN, Node(self.start))
        curNode = Node()
        steps = 0
        while len(self.OPEN) > 0 and steps < self.max_steps and (curNode.i, curNode.j) != self.goal:
            curNode = heappop(self.OPEN)
            steps += 1
            for dirs in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                testNode = (curNode.i + dirs[0], curNode.j + dirs[1])
                if testNode not in self.obstacles and testNode not in self.CLOSED and testNode not in self.other_agents:
                    h = abs(testNode[0] - self.goal[0]) + abs(testNode[1] - self.goal[1])  # Манхэттеновская метрика
                    heappush(self.OPEN, Node(testNode, curNode.g + 1, h))
                    self.CLOSED[testNode] = (curNode.i, curNode.j)  # сохранить информацию о предшествующем узле

    def next_node(self):
        next_node = self.start  # если путь не найден, вернется текущая старт позиция
        if self.goal in self.CLOSED:  # если путь найден
            next_node = self.goal
            while self.CLOSED[next_node] != self.start:
                next_node = self.CLOSED[next_node]
        return next_node

    def update_obstacles(self, obs, other_agents, n):
        obstacles = np.transpose(np.nonzero(obs))                         #получить координаты всех препятствий в текущем наблюдении
        for obstacle in obstacles:
            self.obstacles.add((n[0] + obstacle[0], n[1] + obstacle[1]))  #сохранить их с правильными координатами
        self.other_agents.clear()                                         #забыть ранее увиденных агентов, когда они двигаются
        agents = np.transpose(np.nonzero(other_agents))                   #получить координаты всех агентов, которые видны
        for agent in agents:
            self.other_agents.add((n[0] + agent[0], n[1] + agent[1]))     #сохранить их с правильными координатами


class Model:
    def __init__(self):
        self.lastAction = deque()
        self.agents = None
        self.actions = {tuple(GridConfig().MOVES[i]): i for i in
                        range(len(GridConfig().MOVES))}                 #сделать словарь для перевода координат действий в id

    def act(self, obs, dones, positions_xy, targets_xy) -> list:
        if self.agents is None:
            self.agents = [AStar() for _ in range(len(obs))]            #создать планировщик для каждого из агентов
        actions = []
        for k in range(len(obs)):
            if positions_xy[k] == targets_xy[k]:                        #пропуск агентов, которые уже достигли своих целей
                actions.append(0)
                continue
            self.agents[k].update_obstacles(obs[k][0], obs[k][1], (positions_xy[k][0] - 5, positions_xy[k][1] - 5))
            self.agents[k].best_way(start=positions_xy[k], goal=targets_xy[k])
            next_node = self.agents[k].next_node()
            actions.append(self.actions[(next_node[0] - positions_xy[k][0], next_node[1] - positions_xy[k][1])])
        self.lastAction.append(actions)
        if len(self.lastAction) <= 4:
            return actions
        else:
            self.lastAction.popleft()
        n = 0
        for i in range(len(actions)):
            if (actions[i] != 0 and actions[i] == self.lastAction[1][i] and
            self.lastAction[1][i] == self.lastAction[3][i] and
            self.lastAction[0][i] == self.lastAction[2][i]):
                if n % 2 != 0:
                    actions[i] = 0
                n += 1
        self.lastAction.pop()
        self.lastAction.append(actions)
        return actions
