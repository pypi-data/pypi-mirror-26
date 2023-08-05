# gym-morph

Gym mujoco environments with morphology control.

## Installing

    pip install gym-morph

## Test it out

    import gym, gym_morph
    env = gym.make('Morph-ant-run-v0')
    env.reset()
    while True:
        env.step(env.action_space.sample())  # random actions
        env.render()
