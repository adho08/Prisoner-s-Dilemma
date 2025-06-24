install.packages(c("plotly", "akima", "rgl"))
# Load required libraries
library(plotly)
library(akima)
library(rgl)

# Define the discrete payoff matrix for Player 1
# Based on your matrix: C vs C = 3, C vs D = 0, D vs C = 5, D vs D = 1
payoff_matrix <- matrix(c(3, 0, 5, 1), nrow = 2, byrow = TRUE)
rownames(payoff_matrix) <- c("C", "D")
colnames(payoff_matrix) <- c("C", "D")

print("Discrete Payoff Matrix (Player 1):")
print(payoff_matrix)

# Create discrete points for interpolation
# 0 = full cooperation, 1 = full defection
discrete_points <- expand.grid(
  player1_action = c(0, 1),  # Player 1's action (0=C, 1=D)
  player2_action = c(0, 1)   # Player 2's action (0=C, 1=D)
)

# Assign payoffs based on the matrix
discrete_points$payoff <- c(
  payoff_matrix[1,1],  # C,C -> 3
  payoff_matrix[1,2],  # C,D -> 0
  payoff_matrix[2,1],  # D,C -> 5
  payoff_matrix[2,2]   # D,D -> 1
)

print("Discrete points for interpolation:")
print(discrete_points)

# Create a fine grid for the continuous surface
n_points <- 50
x_seq <- seq(0, 1, length.out = n_points)
y_seq <- seq(0, 1, length.out = n_points)
grid <- expand.grid(x = x_seq, y = y_seq)

# Interpolate using bilinear interpolation
interpolated <- interp(
  x = discrete_points$player1_action,
  y = discrete_points$player2_action,
  z = discrete_points$payoff,
  xo = x_seq,
  yo = y_seq,
  linear = TRUE
)

# Method 1: Using plotly for interactive 3D surface
fig_plotly <- plot_ly(
  x = ~interpolated$x,
  y = ~interpolated$y,
  z = ~interpolated$z,
  type = "surface",
  colorscale = "Viridis"
) %>%
  layout(
    title = "Iterated Continuous Prisoner's Dilemma - Payoff Surface",
    scene = list(
      xaxis = list(title = "Player 1 Action (0=Cooperate, 1=Defect)"),
      yaxis = list(title = "Player 2 Action (0=Cooperate, 1=Defect)"),
      zaxis = list(title = "Player 1 Payoff")
    )
  )

# Display the plotly figure
fig_plotly

# Method 2: Using base R persp() for static 3D plot
dev.new()
persp(
  x = interpolated$x,
  y = interpolated$y,
  z = interpolated$z,
  theta = 45,
  phi = 30,
  col = "lightblue",
  border = "black",
  ticktype = "detailed",
  xlab = "Player 1 Action",
  ylab = "Player 2 Action",
  zlab = "Payoff",
  main = "ICPD Payoff Surface"
)

# Method 3: Using rgl for interactive 3D (alternative)
# Uncomment the following lines if you want to use rgl
# open3d()
# surface3d(
#   x = interpolated$x,
#   y = interpolated$y,
#   z = interpolated$z,
#   col = "lightblue",
#   alpha = 0.8
# )
# axes3d()
# title3d(main = "ICPD Payoff Surface", xlab = "Player 1", ylab = "Player 2", zlab = "Payoff")

# Method 4: Contour plot (2D representation)
dev.new()
filled.contour(
  x = interpolated$x,
  y = interpolated$y,
  z = interpolated$z,
  color = terrain.colors,
  xlab = "Player 1 Action (0=Cooperate, 1=Defect)",
  ylab = "Player 2 Action (0=Cooperate, 1=Defect)",
  main = "ICPD Payoff Surface - Contour Plot"
)

# Alternative: Custom bilinear interpolation function
bilinear_interpolation <- function(x, y) {
  # Bilinear interpolation formula for the payoff matrix
  # f(x,y) = f(0,0)(1-x)(1-y) + f(1,0)x(1-y) + f(0,1)(1-x)y + f(1,1)xy
  payoff <- payoff_matrix[1,1] * (1-x) * (1-y) +  # C,C
            payoff_matrix[2,1] * x * (1-y) +        # D,C
            payoff_matrix[1,2] * (1-x) * y +        # C,D
            payoff_matrix[2,2] * x * y              # D,D
  return(payoff)
}

# Create surface using custom function
x_grid <- outer(x_seq, rep(1, length(y_seq)))
y_grid <- outer(rep(1, length(x_seq)), y_seq)
z_custom <- bilinear_interpolation(x_grid, y_grid)

# Plot using custom interpolation
fig_custom <- plot_ly(
  x = ~x_seq,
  y = ~y_seq,
  z = ~z_custom,
  type = "surface",
  colorscale = "RdYlBu"
) %>%
  layout(
    title = "ICPD Payoff Surface (Custom Bilinear Interpolation)",
    scene = list(
      xaxis = list(title = "Player 1 Action (0=Cooperate, 1=Defect)"),
      yaxis = list(title = "Player 2 Action (0=Cooperate, 1=Defect)"),
      zaxis = list(title = "Player 1 Payoff")
    )
  )

fig_custom

# Print some analysis
cat("\nPayoff Analysis:\n")
cat("Mutual Cooperation (0,0):", bilinear_interpolation(0, 0), "\n")
cat("Player 1 Defects, Player 2 Cooperates (1,0):", bilinear_interpolation(1, 0), "\n")
cat("Player 1 Cooperates, Player 2 Defects (0,1):", bilinear_interpolation(0, 1), "\n")
cat("Mutual Defection (1,1):", bilinear_interpolation(1, 1), "\n")
cat("Mixed Strategy (0.5, 0.5):", bilinear_interpolation(0.5, 0.5), "\n")o
