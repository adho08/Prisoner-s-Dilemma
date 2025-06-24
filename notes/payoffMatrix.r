# Continuous form of the payoff matrix game
# x, y ∈ [0,1] where 1 = Cooperate, 0 = Defect

# Create strategy space
x <- seq(0, 1, length.out = 50)  # Player 1's strategy
y <- seq(0, 1, length.out = 50)  # Player 2's strategy

r = 3L
s = 0L
t = 5L
p = 1L

# Player 1's payoff function: u1(x,y) = 1 - x + 4y - xy
u1 <- outer(x, y, function(x, y) r*x*y + s*x*(1-y) + t*(1-x)*y + p*(1-x)*(1-y))

# Player 2's payoff function: u2(x,y) = 1 + 4x - y - xy  
u2 <- outer(x, y, function(x, y) 1 + 4*x - y - x*y)

# Alternative: Single plot showing one player's payoff
pdf("player1_payoff_surface.pdf", width = 8, height = 6)
persp(x, y, u1,
	theta = 30,
	phi = 30,
	col = "lightblue",
	shade = 0.75,
	ticktype = "detailed",
	xlim = c(0, 1),
	ylim = c(0, 1),
	xlab = "Player 1 Strategy (x)",
	ylab = "Player 2 Strategy (y)",
	zlab = "Player 1 Payoff",
	main = "Payoff surface of the Iterated Continuous Prisoner's Dilemma of Player 1")
