import gymnasium
import time
from stable_baselines3 import PPO
from stable_baselines3 import SAC
from stable_baselines3.common.env_util import make_vec_env

from go1_mujoco_env import Go1MujocoEnv

def train(total_timesteps=100000, model_save_path="./models/model", log_save_path="./tensorboard/log"):

    start_time = time.time()

    env = make_vec_env(
        Go1MujocoEnv,
    )

    model = SAC("MlpPolicy", env, verbose=1, tensorboard_log=log_save_path, device="cpu")

    model.learn(total_timesteps=total_timesteps)

    model.save(model_save_path)
    print(f"Model saved to {model_save_path}")

    end_time = time.time()
    total_time = end_time - start_time
    hours, rem = divmod(total_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print(f"\nTraining completed in: {int(hours)}h {int(minutes)}m {int(seconds)}s")

    return model

def evaluate(model, num_episodes=10):
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

    # model = train(total_timesteps=2000000, model_save_path="./models/go1_huashan_200w", log_save_path="tensorboard/go1_huashan_200w")

    test("./models/go1_huashan_200w", num_steps=1000)

    # evaluate(model, num_episodes=5)
    