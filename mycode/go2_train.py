import gymnasium
from stable_baselines3 import PPO

env = gymnasium.make(
    'Ant-v5',
    xml_file='./unitree_go2/go2_change.xml',
    # xml_file='~/code/Mujoco-RL/terrain/model/go2_ditch.xml',
    forward_reward_weight=1,
    ctrl_cost_weight=0.05,
    contact_cost_weight=5e-4,
    healthy_reward=1,
    main_body=1,
    healthy_z_range=(0.195, 0.75),
    include_cfrc_ext_in_observation=True,
    exclude_current_positions_from_observation=False,
    reset_noise_scale=0.1,
    frame_skip=25,
    max_episode_steps=1000,
    render_mode="human",
)

def train(env_name, total_timesteps=100000, model_save_path="./models/model", log_save_path="./tensorboard/log"):

    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_save_path, device="cpu")

    model.learn(total_timesteps=total_timesteps)

    model.save(model_save_path)
    print(f"Model saved to {model_save_path}")

    return model

def evaluate(env_name, model, num_episodes=10):
    total_rewards = []

    for episode in range(num_episodes):
        obs, info = env.reset()
        episode_reward = 0
        done = False
        while not done:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, truncated, info = env.step(action)
            episode_reward += reward
            if done or truncated:
                break
        total_rewards.append(episode_reward)
        print(f"Episode {episode + 1}: Reward: {episode_reward}")

    avg_reward = sum(total_rewards) / num_episodes
    print(f"Average reward over {num_episodes} episodes: {avg_reward}")

    env.close()

def test(env_name, model, num_steps=1000):
    obs, info = env.reset()

    for i in range(num_steps):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, truncated, info = env.step(action)
        env.render()
        if done or truncated:
            obs, info = env.reset()

    env.close()

if __name__ == "__main__":

    model = train('Ant-v5', total_timesteps=1000000, model_save_path="./models/go2_huashan", log_save_path="tensorboard/go2_huashan")

    # model = PPO.load("./models/ppo_ant_ditch")

    # test('Ant-v5' ,model, num_steps=1000)

    # evaluate('Ant-v4', model, num_episodes=5)
    