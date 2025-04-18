# Load required libraries
library(dplyr)
library(ggplot2)

# Read the CSV file
# Since it has headers and is comma-separated
data <- read.csv("/mnt/c/Users/adhos/Onedrive - Gymnasium Thun/Maturaarbeit/PD/data/results.csv")

# Create a barplot
ggplot(data, aes(x = strategy, y = points, fill = strategy)) +
  geom_bar(stat = "identity") +
  theme_minimal() +
  labs(
    title = "Strategy Points Comparison",
    x = "Strategy",
    y = "Points"
  ) +
  theme(legend.position = "none")

ggsave("plot.png")
