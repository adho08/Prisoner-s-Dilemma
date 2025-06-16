# Suppress text output from r script. This will not show errors
sink(file("/dev/null", "w"), type="message")

# Load required libraries
library(dplyr)
library(ggplot2)

# Read the CSV file
# Since it has headers and is comma-separated
data <- read.csv("/mnt/c/Users/adhos/Onedrive - Gymnasium Thun/Maturaarbeit/PD/IPD/data/results.csv")

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
