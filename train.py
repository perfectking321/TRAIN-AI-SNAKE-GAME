"""
Snake AI — DQN Training
Run:  python train.py
"""
import matplotlib
matplotlib.use('TkAgg')          # live window; change to Qt5Agg if you have pyqt5
import matplotlib.pyplot as plt

from src.agent import Agent
from src.game import SnakeGameAI


def train():
    scores      = []
    mean_scores = []
    total       = 0
    agent       = Agent()
    game        = SnakeGameAI()

    # ── Live plot setup ──────────────────────────────────────────────
    plt.ion()
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.canvas.manager.set_window_title('Snake AI — Training')

    def refresh_plot():
        ax.clear()
        ax.set_title('Score over Games')
        ax.set_xlabel('Game')
        ax.set_ylabel('Score')
        ax.plot(scores,      label='Score',      color='steelblue')
        ax.plot(mean_scores, label='Mean Score', color='orange', linestyle='--')
        if scores:
            ax.text(len(scores) - 1,      scores[-1],      str(scores[-1]),      fontsize=8)
        if mean_scores:
            ax.text(len(mean_scores) - 1, mean_scores[-1], f'{mean_scores[-1]:.1f}', fontsize=8)
        ax.legend()
        ax.set_ylim(bottom=0)
        plt.tight_layout()
        plt.pause(0.001)
    # ─────────────────────────────────────────────────────────────────

    while True:
        state_old  = agent.get_state(game)
        move       = agent.get_action(state_old)
        reward, done, score = game.play_step(move)
        state_new  = agent.get_state(game)

        agent.train_short_memory(state_old, move, reward, state_new, done)
        agent.remember(state_old, move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            scores.append(score)
            total    += score
            mean      = total / agent.n_games
            mean_scores.append(mean)

            if score >= agent.record:
                agent.record = score
                agent.model.save(record=agent.record,
                                 n_games=agent.n_games,
                                 mean_score=mean)

            print(f'Game {agent.n_games:4d} | Score {score:3d} | Record {agent.record:3d} | Mean {mean:.2f}')
            refresh_plot()


if __name__ == '__main__':
    train()
