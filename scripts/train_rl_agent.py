import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecTransposeImage
from src.rl_agent.airsim_env import AirSimForestEnv
from stable_baselines3.common.policies import ActorCriticCnnPolicy
from src.utils.training_manager import TrainingManager
import os

def train_ppo_cnn():
    """
    Trains the PPO agent with a custom CNN policy in the AirSim environment, managed by TrainingManager for configuration and checkpointing
    """

    manager = TrainingManager()
    config = manager.config

    env = AirSimForestEnv(config=config)

    model = PPO(ActorCriticCnnPolicy, env,
        batch_size=config['training']['batch_size'],
        learning_rate=config['training']['learning_rate'],
        verbose=1,
        tensorboard_log="./ppo_cnn_tensorboard/"
    )

    loaded_model, start_episode = manager.load_latest_checkpoint(PPO(ActorCriticCnnPolicy, env))
    if loaded_model:
        model = loaded_model
        print(f"Resuming training from episode {start_episode}")
    else:
        start_episode = 0
        print("Starting training from scratch.")

    
    max_episodes = config['training']['max_episodes']
    for episode in range(start_episode + 1, max_episodes + 1):
        print(f"Starting episode {episode}/{max_episdode}")
        model.learn(total_timesteps=10000, reset_num_timesteps=False)
        metrics = {'episode_reward_mean': 0}
        manager.save_checkpoint(model.policy, metrics, episode)

    print("PPO CNN training finished.")
    env.close()

if __name__ == "__main__":
    train_ppo_cnn()