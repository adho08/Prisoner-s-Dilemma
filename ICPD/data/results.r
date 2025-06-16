# Suppress text output from r script. This will not show errors
sink(file("/dev/null", "w"), type="message")

# Load required libraries
library(dplyr)
library(ggplot2)

# Read the CSV file
data <- read.csv("/mnt/c/Users/adhos/Onedrive - Gymnasium Thun/Maturaarbeit/Axelrods-Tournament/ICPD/data/results.csv")

# Reorder strategy factor by points (descending order)
data$strategy <- reorder(data$strategy, -data$points)

# Merge the data of points with the data of attributes
attributes <- read.csv("strategies_attributes.csv")
data <- merge(data, attributes, by = "strategy")

# Calculate text size based on number of bars (strategies)
text_size <- max(2, min(6, 20 / nrow(data)))

# Create a column to categorize strategies above/below median
data$Seperation <- ifelse(data$points >= median(data$points), "Above Median", "Below Median")
# Create a barplot
ggplot(data, aes(x = strategy, y = points, fill = Seperation)) +
	geom_bar(stat = "identity", color = "black", size = 0.5) +
	geom_text(aes(label = points), vjust = 2.5, color = "black", size = text_size)+
	theme_minimal() +
	guides(color = "none") +
	scale_fill_manual(values = c("Above Median" = "green", "Below Median" = "red")) +
	labs(
	     title = "Strategy Points Comparison",
	     x = "Strategy",
	     y = "Points"
	     ) +
	theme(legend.position = "top")

ggsave("./plots/plotMedian.png")

# Create a barplot
ggplot(data, aes(x = strategy, y = points, fill = nice)) +
	geom_bar(stat = "identity", color = "black", size = 0.5) +
	geom_text(aes(label = points), vjust = 2.5, color = "black", size = text_size)+
	theme_minimal() +
	guides(color = "none") +
	scale_fill_manual(values = c("True" = "green", "False" = "red")) +
	labs(
	     title = "Strategy Points Comparison",
	     x = "Strategy",
	     y = "Points"
	     ) +
	theme(legend.position = "top")

ggsave("./plots/plotNice.png")

# Create a barplot
ggplot(data, aes(x = strategy, y = points, fill = retaliates)) +
	geom_bar(stat = "identity", color = "black", size = 0.5) +
	geom_text(aes(label = points), vjust = 2.5, color = "black", size = text_size)+
	theme_minimal() +
	guides(color = "none") +
	scale_fill_manual(values = c("True" = "green", "False" = "red")) +
	labs(
	     title = "Strategy Points Comparison",
	     x = "Strategy",
	     y = "Points"
	     ) +
	theme(legend.position = "top")

ggsave("./plots/plotRetaliates.png")

# Create a barplot
ggplot(data, aes(x = strategy, y = points, fill = forgiving)) +
	geom_bar(stat = "identity", color = "black", size = 0.5) +
	geom_text(aes(label = points), vjust = 2.5, color = "black", size = text_size)+
	theme_minimal() +
	guides(color = "none") +
	scale_fill_manual(values = c("True" = "green", "False" = "red")) +
	labs(
	     title = "Strategy Points Comparison",
	     x = "Strategy",
	     y = "Points"
	     ) +
	theme(legend.position = "top")

ggsave("./plots/plotForgiving.png")

# Create a barplot
ggplot(data, aes(x = strategy, y = points, fill = envious)) +
	geom_bar(stat = "identity", color = "black", size = 0.5) +
	geom_text(aes(label = points), vjust = 2.5, color = "black", size = text_size)+
	theme_minimal() +
	guides(color = "none") +
	scale_fill_manual(values = c("True" = "red", "False" = "green")) +
	labs(
	     title = "Strategy Points Comparison",
	     x = "Strategy",
	     y = "Points"
	     ) +
	theme(legend.position = "top")

ggsave("./plots/plotEnvious.png")
