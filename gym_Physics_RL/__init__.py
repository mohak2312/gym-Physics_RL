from gym.envs.registration import register

register(
    id='Physics_RL-v0',
    entry_point='gym_Physics_RL.envs:Physics_RLEnv',
    timestep_limit=2000,
)
register(
    id='Physics_RL-extrahard-v0',
    entry_point='gym_Physics_RL.envs:Physics_RLExtraHardEnv',
    timestep_limit=2000,
)
