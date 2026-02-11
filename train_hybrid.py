"""
Train the hybrid DQN + Hamiltonian agent to play Snake
"""
from src.agent_hybrid import HybridAgent
from src.game import SnakeGameAI
from src.helper import plot

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    agent = HybridAgent(use_hamiltonian=True)
    game = SnakeGameAI()
    
    while True:
        # get old state
        state_old = agent.get_state(game)
        
        # get move
        final_move = agent.get_action(state_old)
        
        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        
        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        
        # remember
        agent.remember(state_old, final_move, reward, state_new, done)
        
        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            
            if score > agent.record:
                agent.record = score
                agent.model.save(
                    record=agent.record, 
                    n_games=agent.n_games, 
                    mean_score=total_score/agent.n_games,
                    folder=agent.model_folder
                )
            
            print(f'Game {agent.n_games} Score {score} Record: {agent.record}')
            print(f'AI Decisions: {agent.ai_decisions} | Hamiltonian: {agent.hamiltonian_uses}')
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()
