from copy import deepcopy
from ding.entry import serial_pipeline
from easydict import EasyDict

pong_acer_config = dict(
    env=dict(
        collector_env_num=16,
        evaluator_env_num=4,
        n_evaluator_episode=8,
        stop_value=20,
        env_id='PongNoFrameskip-v4',
        frame_stack=4,
        manager=dict(shared_memory=False, )
    ),
    policy=dict(
        cuda=True,
        on_policy=False,
        priority=False,
        model=dict(
            obs_shape=[4, 84, 84],
            action_shape=6,
            encoder_hidden_size_list=[128, 128, 512],
            critic_head_hidden_size=512,
            critic_head_layer_num=2,
            actor_head_hidden_size=512,
            actor_head_layer_num=2,
        ),
        unroll_len=32,
        learn=dict(
            # (int) collect n_sample data, train model update_per_collect times
            # here we follow impala serial pipeline
            update_per_collect=10,
            # (int) the number of data for a train iteration
            batch_size=64,
            # grad_clip_type='clip_norm',
            # clip_value=10,
            learning_rate_actor=0.0001,
            learning_rate_critic=0.0003,
            # (float) loss weight of the value network, the weight of policy network is set to 1
            # (float) loss weight of the entropy regularization, the weight of policy network is set to 1
            entropy_weight=0.01,
            # (float) discount factor for future reward, defaults int [0, 1]
            discount_factor=0.9,
            # (float) additional discounting parameter
            trust_region=True,
            # (float) clip ratio of importance weights
            # (float) clip ratio of importance weights
            c_clip_ratio=10,
        ),
        collect=dict(
            # (int) collect n_sample data, train model n_iteration times
            n_sample=16,
            # (float) discount factor for future reward, defaults int [0, 1]
            discount_factor=0.9,
            collector=dict(collect_print_freq=1000, ),
        ),
        eval=dict(evaluator=dict(eval_freq=5000, )),
        other=dict(replay_buffer=dict(
            type='naive',
            replay_buffer_size=10000,
        ), ),
    ),
)
main_config = EasyDict(pong_acer_config)

pong_acer_create_config = dict(
    env=dict(
        type='atari',
        import_names=['dizoo.atari.envs.atari_env'],
    ),
    env_manager=dict(type='subprocess'),
    policy=dict(type='acer'),
)
create_config = EasyDict(pong_acer_create_config)

if __name__ == '__main__':
    serial_pipeline((main_config, create_config), seed=0)
