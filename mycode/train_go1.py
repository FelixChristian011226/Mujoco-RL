import gymnasium
from stable_baselines3 import PPO
from stable_baselines3 import SAC
from stable_baselines3.common.env_util import make_vec_env

from go1_mujoco_env import Go1MujocoEnv

def train(env_name, total_timesteps=100000, model_save_path="./models/model", log_save_path="./tensorboard/log"):

    env = make_vec_env(
        Go1MujocoEnv,
    )

    # model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_save_path, device="cpu")
    model = SAC("MlpPolicy", env, verbose=1, tensorboard_log=log_save_path, device="cpu")

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

def test(model_path, num_steps=1000):

    env = Go1MujocoEnv(
        render_mode="human",
    )

    model = SAC.load(path=model_path, env=env, verbose=1, device="cpu")

    obs, _ = env.reset()

    for i in range(num_steps):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, truncated, info = env.step(action)
        env.render()
        if done or truncated:
            obs, _ = env.reset()

    env.close()

if __name__ == "__main__":

    # model = train('Ant-v5', total_timesteps=100000, model_save_path="./models/go2_floor", log_save_path="tensorboard/go2_floor")

    test("./models/go2_floor", num_steps=1000)

    # evaluate('Ant-v4', model, num_episodes=5)
    