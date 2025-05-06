import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def continuous_pd_payoff(coop_level1, coop_level2, R=3, S=0, T=5, P=1):
    """
    Calculate payoffs for continuous prisoner's dilemma
    
    Parameters:
    - coop_level1: cooperation level of player 1 (between 0 and 1)
    - coop_level2: cooperation level of player 2 (between 0 and 1)
    - R: Reward for mutual cooperation
    - S: Sucker's payoff (cooperation while other defects)
    - T: Temptation to defect
    - P: Punishment for mutual defection
    
    Returns:
    - payoff1: payoff for player 1
    - payoff2: payoff for player 2
    """
    # Player 1's payoff
    payoff1 = coop_level1 * coop_level2 * R + \
              coop_level1 * (1 - coop_level2) * S + \
              (1 - coop_level1) * coop_level2 * T + \
              (1 - coop_level1) * (1 - coop_level2) * P
    
    # Player 2's payoff
    payoff2 = coop_level2 * coop_level1 * R + \
              coop_level2 * (1 - coop_level1) * S + \
              (1 - coop_level2) * coop_level1 * T + \
              (1 - coop_level2) * (1 - coop_level1) * P
    
    return payoff1, payoff2

# Create a grid of cooperation levels
resolution = 100
coop_levels = np.linspace(0, 1, resolution)
X, Y = np.meshgrid(coop_levels, coop_levels)

# Calculate payoffs for all combinations
payoff1 = np.zeros((resolution, resolution))
payoff2 = np.zeros((resolution, resolution))

for i in range(resolution):
    for j in range(resolution):
        payoff1[i, j], payoff2[i, j] = continuous_pd_payoff(X[i, j], Y[i, j])

# Create 3D plots
fig = plt.figure(figsize=(15, 6))

# Player 1's payoff
ax1 = fig.add_subplot(121, projection='3d')
surf1 = ax1.plot_surface(X, Y, payoff1, cmap=cm.coolwarm, linewidth=0, antialiased=True)
ax1.set_xlabel('Player 1 Cooperation')
ax1.set_ylabel('Player 2 Cooperation')
ax1.set_zlabel('Player 1 Payoff')
ax1.set_title("Player 1's Payoff")
fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=5)

# Player 2's payoff
ax2 = fig.add_subplot(122, projection='3d')
surf2 = ax2.plot_surface(X, Y, payoff2, cmap=cm.coolwarm, linewidth=0, antialiased=True)
ax2.set_xlabel('Player 1 Cooperation')
ax2.set_ylabel('Player 2 Cooperation')
ax2.set_zlabel('Player 2 Payoff')
ax2.set_title("Player 2's Payoff")
fig.colorbar(surf2, ax=ax2, shrink=0.5, aspect=5)

plt.tight_layout()
plt.show()

# Let's also create a plot of total social welfare (sum of payoffs)
plt.figure(figsize=(10, 8))
social_welfare = payoff1 + payoff2
plt.contourf(X, Y, social_welfare, 20, cmap='viridis')
plt.colorbar(label='Total Payoff (Social Welfare)')
plt.xlabel('Player 1 Cooperation')
plt.ylabel('Player 2 Cooperation')
plt.title('Social Welfare in Continuous Prisoner\'s Dilemma')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Create a heatmap showing Player 1's best response to Player 2's choices
plt.figure(figsize=(8, 8))
# For each Player 2 cooperation level, find Player 1's best cooperation level
best_response = np.zeros(resolution)
for j in range(resolution):
    player2_coop = coop_levels[j]
    max_payoff = -np.inf
    best_coop = 0
    
    # Check all possible responses by Player 1
    for i in range(resolution):
        player1_coop = coop_levels[i]
        p1, _ = continuous_pd_payoff(player1_coop, player2_coop)
        if p1 > max_payoff:
            max_payoff = p1
            best_coop = player1_coop
    
    best_response[j] = best_coop

plt.plot(coop_levels, best_response, 'r-', linewidth=3)
plt.plot([0, 1], [0, 1], 'k--', alpha=0.5)  # Diagonal line for reference
plt.xlabel('Player 2 Cooperation Level')
plt.ylabel('Best Response of Player 1')
plt.title('Player 1\'s Best Response Function')
plt.grid(True)
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.tight_layout()
plt.show()
