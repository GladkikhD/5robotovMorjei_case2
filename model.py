from collections import deque
from pogema import GridConfig
from astar import AStar

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
