from copy import deepcopy
from ding.entry import serial_pipeline
from easydict import EasyDict

agent_num = 8
collector_env_num = 16
evaluator_env_num = 8

main_config = dict(
    env=dict(
        map_name='3s5z',
        difficulty=7,
        reward_only_positive=True,
        mirror_opponent=False,
        agent_num=agent_num,
        collector_env_num=collector_env_num,
        evaluator_env_num=evaluator_env_num,
        shared_memory=False,
        stop_value=0.999,
        n_evaluator_episode=32,
    ),
    policy=dict(
        model=dict(
            agent_num=agent_num,
            obs_shape=150,
            global_obs_shape=216,
            action_shape=14,
            hidden_size_list=[64],
            embedding_size=64,
            lstm_type='gru',
            dueling=False,
        ),
        learn=dict(
            multi_gpu=False,
            update_per_collect=20,
            batch_size=32,
            learning_rate=0.0005,
            double_q=True,
            target_update_theta=0.006,
            discount_factor=0.95,
            td_weight=1,
            opt_weight=0.1,
            nopt_min_weight=0.0001,
        ),
        collect=dict(
            n_episode=32,
            unroll_len=10,
            env_num=collector_env_num,
        ),
        eval=dict(env_num=evaluator_env_num, evaluator=dict(eval_freq=100, )),
        other=dict(
            eps=dict(
                type='linear',
                start=1,
                end=0.05,
                decay=10000,
            ),
            replay_buffer=dict(
                replay_buffer_size=15000,
                # (int) The maximum reuse times of each data
                max_reuse=1e+9,
                max_staleness=1e+9,
            ),
        ),
    ),
)
main_config = EasyDict(main_config)
create_config = dict(
    env=dict(
        type='smac',
        import_names=['dizoo.smac.envs.smac_env'],
    ),
    env_manager=dict(type='subprocess'),
    policy=dict(type='qtran'),
    collector=dict(type='episode', get_train_sample=True),
)
create_config = EasyDict(create_config)


def train(args):
    config = [main_config, create_config]
    serial_pipeline(config, seed=args.seed)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', '-s', type=int, default=0)
    args = parser.parse_args()

    train(args)
