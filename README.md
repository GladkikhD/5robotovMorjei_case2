# <p align="center"> :sparkles: POGEMA-Based Neural Network :sparkles: </p>

![LOGO](https://i.ibb.co/MV3H79q/1.png)

## Neural Network for optimal route building used in multiple agents system

> This repo is created for AI Hackaton on May, 27-29, 2022, coworking area of Pacific National University, KHV.

### Solution

In our work, the problem of the interaction of several robots working independently of each other is raised. We, using the A\* optimal control algorithm, build routes for each robot in such a way as to optimize their collective functioning (collision-free movement).

Based on the results of the work, a working prototype was created, as well as animated images that allow visualizing the work of the prototype. The proposed solution allows us to achieve autonomous operation of robots and quickly resolve collisions if they occur.

The neural network is implemented on the basis of the RL learning method without a teacher using the optimal control technology.

### Uniqueness

In our work, the "author's" method of resolving collisions is used, based on the analysis of the previous actions of an individual agent and the decision to suspend its execution of the task if this is required to resolve the collision that has arisen.

### Technology stack

Python programming language; Google Collab; Libraries gym, pogema, numpy; PyCharm; VS Code; A\* (AStar); Reinforcement Learning.

## Requirements

### Python packages

- pogema
- gym
- numpy

## Launch

```
git clone https://github.com/GladkikhD/5robotovMorjei_case2

cd ./5robotovMorjei_case2

python ./test.py
```

# Links

- Based on [pogema repository](https://github.com/AIRI-Institute/pogema)

---

> **POGEMA-Based Neural Network by team _«5robotovMorjei»_** :smiley_cat: :

> - Balabasova Alisa ([@alice-bal](https://github.com/alice-bal)) 
> - Gladkikh Dmitry ([@GladkikhD](https://github.com/GladkikhD)) 
> - Mysov Nikita ([@suraifokkusu](https://github.com/suraifokkusu)) 
> - Sirotkin Egor ([@warfka](https://github.com/warfka))