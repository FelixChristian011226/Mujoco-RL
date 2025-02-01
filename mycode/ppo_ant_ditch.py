import gymnasium as gym
from stable_baselines3 import PPO

def train(env_name, total_timesteps=1000000, model_save_path="./models/ppo_ant"):
    # env = gym.make(env_name, render_mode="human")
    # env = gym.make(env_name, xml_file="~/coding/Mujoco-RL/mycode/ant.xml", render_mode="human")
    env = gym.make(env_name, xml_file="~/coding/Mujoco-RL/terrain/model/ant_ditch.xml", render_mode="human")

    # model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./ppo_ant_tensorboard/")
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./tensorboard/ppo_ant_ditch")

    model.learn(total_timesteps=total_timesteps)

    model.save(model_save_path)
    print(f"Model saved to {model_save_path}")

    return model

def evaluate(env_name, model, num_episodes=10):
    # env = gym.make(env_name)
    # env = gym.make(env_name, xml_file="~/coding/Mujoco-RL/mycode/ant.xml", render_mode="human")
    env = gym.make(env_name, xml_file="~/coding/Mujoco-RL/terrain/model/ant_ditch.xml", render_mode="human")
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
    #env = gym.make(env_name, render_mode="human")
    # env = gym.make(env_name, xml_file="~/coding/Mujoco-RL/mycode/ant.xml", render_mode="human")
    env = gym.make(env_name, xml_file="~/coding/Mujoco-RL/terrain/model/ant_ditch.xml", render_mode="human")
    obs, info = env.reset()

    for i in range(num_steps):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, truncated, info = env.step(action)
        env.render()
        if done or truncated:
            obs, info = env.reset()

    env.close()

if __name__ == "__main__":

    # model = train('Ant-v4', total_timesteps=1000000, model_save_path="./models/ppo_ant")
    # model = train('Ant-v4', total_timesteps=1000000, model_save_path="./models/ppo_ant_stairs")
    model = train('Ant-v5', total_timesteps=1000000, model_save_path="./models/ppo_ant_ditch")

    # model = PPO.load("./models/ppo_ant_ditch")

    test('Ant-v5' ,model, num_steps=1000)

    # evaluate('Ant-v4', model, num_episodes=5)
