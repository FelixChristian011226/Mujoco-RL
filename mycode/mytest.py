import gymnasium as gym
from stable_baselines3 import PPO
import time

env = gym.make('Ant-v4', render_mode="human")

model = PPO("MlpPolicy", env, verbose=1)

start_time=time.time()
model.learn(total_timesteps=1000000)
end_time=time.time()

total_time = end_time - start_time
total_time_minutes = total_time / 60
print(f"总训练时间: {total_time_minutes:.2f} 分钟")

model.save("ppo_ant")
model.save("./models/ppo_ant")
print("Model saved to ./models/ppo_ant")

model = PPO.load("ppo_ant")

obs, info = env.reset()
for i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, truncated, info = env.step(action)
    env.render()
    if done:
        obs, info = env.reset()
