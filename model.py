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
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f or ((self.f == other.f) and (self.g < other.g))


class AStar:
    def __init__(self):
        self.start = (0, 0)
        self.goal = (0, 0)
        self.max_steps = 10000  # due to the absence of information about the map size we need some other stop criterion
        self.OPEN = list()
        self.CLOSED = dict()
        self.obstacles = set()
        self.other_agents = set()

    def compute_shortest_path(self, start, goal):
        self.start = start
        self.goal = goal
        self.CLOSED = dict()
        self.OPEN = list()
        heappush(self.OPEN, Node(self.start))
        u = Node()
        steps = 0
        while len(self.OPEN) > 0 and steps < self.max_steps and (u.i, u.j) != self.goal:
            u = heappop(self.OPEN)
            steps += 1
            for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                n = (u.i+d[0], u.j + d[1])
                if n not in self.obstacles and n not in self.CLOSED and n not in self.other_agents:
                    h = abs(n[0] - self.goal[0]) + abs(n[1] - self.goal[1])  # Manhattan distance as a heuristic function
                    heappush(self.OPEN, Node(n, u.g + 1, h))
                    self.CLOSED[n] = (u.i, u.j)  # store information about the predecessor

    def get_next_node(self):
        next_node = self.start  # if path not found, current start position is returned
        if self.goal in self.CLOSED:  # if path found
            next_node = self.goal
            while self.CLOSED[next_node] != self.start:  # get node in the path with start node as a predecessor
                next_node = self.CLOSED[next_node]
        return next_node

    def update_obstacles(self, obs, other_agents, n):
        obstacles = np.transpose(np.nonzero(obs))  # get the coordinates of all obstacles in current observation
        for obstacle in obstacles:
            self.obstacles.add((n[0] + obstacle[0], n[1] + obstacle[1]))  # save them with correct coordinates
        self.other_agents.clear()  # forget previously seen agents as they move
        agents = np.transpose(np.nonzero(other_agents))  # get the coordinates of all agents that are seen
        for agent in agents:
            self.other_agents.add((n[0] + agent[0], n[1] + agent[1]))  # save them with correct coordinates


class Model:
    def __init__(self):
        self.lastAction = deque()
        self.agents = None
        self.actions = {tuple(GridConfig().MOVES[i]): i for i in
                        range(len(GridConfig().MOVES))}  # make a dictionary to translate coordinates of actions into id

    def act(self, obs, dones, positions_xy, targets_xy) -> list:
        if self.agents is None:
            self.agents = [AStar() for _ in range(len(obs))]  # create a planner for each of the agents
        actions = []
        for k in range(len(obs)):
            if positions_xy[k] == targets_xy[k]:  # don't waste time on the agents that have already reached their goals
                actions.append(0)  # just add useless action to save the order and length of the actions
                continue
            self.agents[k].update_obstacles(obs[k][0], obs[k][1], (positions_xy[k][0] - 5, positions_xy[k][1] - 5))
            self.agents[k].compute_shortest_path(start=positions_xy[k], goal=targets_xy[k])
            next_node = self.agents[k].get_next_node()
            actions.append(self.actions[(next_node[0] - positions_xy[k][0], next_node[1] - positions_xy[k][1])])
        #self.prevAction = self.lastAction
        #self.lastAction = actions[len(actions) - 1]
        self.lastAction.append(actions)
        #if len(self.lastAction) > 3 and actions == self.lastAction[1] and self.lastAction[1] == self.lastAction[3]:
        #    n = 0
        #    for i in range(len(actions)):
        #        if actions[i] != 0:
        #            if n % 2 != 0:
        #                actions[i] = 0
        #            n += 1
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
