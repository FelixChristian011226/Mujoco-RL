import os
import time
import gymnasium
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback  # 新增导入回调基类

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

# 自定义回调类：每隔指定步数保存模型并删除上一个
class AutoSaveCallback(BaseCallback):
    def __init__(self, check_freq: int, save_path: str, verbose=0):
        super().__init__(verbose)
        self.check_freq = check_freq   # 保存间隔（单位：timesteps）
        self.save_path = save_path     # 模型保存基础路径
        self.last_save = None          # 记录上一个模型的路径

    def _on_step(self) -> bool:
        # 每隔 check_freq 步触发保存
        if self.n_calls % self.check_freq == 0:
            # 生成带时间步的保存路径，例如：./models/go2_huashan_10000
            current_save = f"{self.save_path}_{self.num_timesteps}"
            
            # 保存当前模型
            self.model.save(current_save)
            
            # 如果存在上一个模型文件，则删除
            if self.last_save is not None and os.path.exists(self.last_save + ".zip"):
                os.remove(self.last_save + ".zip")
                if self.verbose > 0:
                    print(f"Deleted previous model: {self.last_save}.zip")
            
            # 更新记录
            self.last_save = current_save
            if self.verbose > 0:
                print(f"Model saved: {current_save}.zip")
        return True

def train(env_name, total_timesteps=100000, model_save_path="./models/model", log_save_path="./tensorboard/log"):
    start_time = time.time()

    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_save_path, device="cpu")
    
    # 创建自动保存回调（每隔 10000 步保存一次）
    autosave_callback = AutoSaveCallback(check_freq=2048, save_path=model_save_path, verbose=1)
    
    # 将回调传入 learn 方法
    model.learn(total_timesteps=total_timesteps, callback=autosave_callback)

    end_time = time.time()
    total_time = end_time - start_time
    hours, rem = divmod(total_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print(f"\nTraining completed in: {int(hours)}h {int(minutes)}m {int(seconds)}s")

    # 训练结束后保存最终模型
    final_save_path = f"{model_save_path}_final"
    model.save(final_save_path)
    print(f"Final model saved to {final_save_path}.zip")

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

    # model = PPO.load("./models/go2_huashan_final", device='cpu')

    # test('Ant-v5' ,model, num_steps=1000)

    # evaluate('Ant-v4', model, num_episodes=5)
    