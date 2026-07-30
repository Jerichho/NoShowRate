#!/usr/bin/env Rscript

# Exploratory Data Analysis Script for Airline No-Show Prediction
# Author: [Your Name]
# Date: [Current Date]

# Load required libraries
library(tidyverse)
library(ggplot2)
library(corrplot)
library(lubridate)
library(scales)

# Set up logging
log_file <- file("eda.log")
sink(log_file, append = TRUE)
sink(log_file, append = TRUE, type = "message")

# Function to load and prepare data
load_data <- function(file_path) {
  tryCatch({
    data <- read.csv(file_path)
    message("Successfully loaded data from ", file_path)
    return(data)
  }, error = function(e) {
    message("Error loading data: ", e$message)
    stop(e)
  })
}

# Function to create no-show rate distribution plot
plot_no_show_distribution <- function(data) {
  p <- ggplot(data, aes(x = no_show)) +
    geom_bar(aes(y = ..prop.., group = 1), fill = "steelblue") +
    scale_y_continuous(labels = percent_format()) +
    labs(title = "Distribution of No-Show Rates",
         x = "No-Show Status",
         y = "Percentage") +
    theme_minimal()
  
  ggsave("../outputs/no_show_distribution.png", p, width = 10, height = 6)
  message("Saved no-show distribution plot")
}

# Function to create correlation heatmap
plot_correlation_heatmap <- function(data) {
  # Select numeric columns
  numeric_data <- data %>% select_if(is.numeric)
  
  # Calculate correlation matrix
  cor_matrix <- cor(numeric_data, use = "complete.obs")
  
  # Create correlation plot
  png("../outputs/correlation_heatmap.png", width = 1200, height = 1200)
  corrplot(cor_matrix, 
           method = "color",
           type = "upper",
           tl.col = "black",
           tl.srt = 45,
           addCoef.col = "black",
           number.cex = 0.7)
  dev.off()
  message("Saved correlation heatmap")
}

# Function to analyze temporal patterns
analyze_temporal_patterns <- function(data) {
  # Convert date columns to Date type
  data$booking_date <- as.Date(data$booking_date)
  data$flight_date <- as.Date(data$flight_date)
  
  # Calculate booking lead time
  data$booking_lead_time <- as.numeric(data$flight_date - data$booking_date)
  
  # Plot no-show rate by booking lead time
  p <- ggplot(data, aes(x = booking_lead_time, y = no_show)) +
    geom_smooth(method = "loess", se = TRUE) +
    labs(title = "No-Show Rate by Booking Lead Time",
         x = "Days Before Flight",
         y = "No-Show Rate") +
    theme_minimal()
  
  ggsave("../outputs/lead_time_analysis.png", p, width = 10, height = 6)
  message("Saved booking lead time analysis plot")
  
  # Analyze day of week patterns
  data$day_of_week <- wday(data$flight_date, label = TRUE)
  
  p <- ggplot(data, aes(x = day_of_week, fill = no_show)) +
    geom_bar(position = "fill") +
    scale_y_continuous(labels = percent_format()) +
    labs(title = "No-Show Rate by Day of Week",
         x = "Day of Week",
         y = "Percentage") +
    theme_minimal()
  
  ggsave("../outputs/day_of_week_analysis.png", p, width = 10, height = 6)
  message("Saved day of week analysis plot")
}

# Function to analyze fare class patterns
analyze_fare_class_patterns <- function(data) {
  p <- ggplot(data, aes(x = fare_class, fill = no_show)) +
    geom_bar(position = "fill") +
    scale_y_continuous(labels = percent_format()) +
    labs(title = "No-Show Rate by Fare Class",
         x = "Fare Class",
         y = "Percentage") +
    theme_minimal()
  
  ggsave("../outputs/fare_class_analysis.png", p, width = 10, height = 6)
  message("Saved fare class analysis plot")
}

# Main function
main <- function() {
  tryCatch({
    # Load data
    data <- load_data("../data/processed/cleaned_data.csv")
    
    # Create output directory if it doesn't exist
    dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)
    
    # Generate plots and analyses
    plot_no_show_distribution(data)
    plot_correlation_heatmap(data)
    analyze_temporal_patterns(data)
    analyze_fare_class_patterns(data)
    
    message("EDA completed successfully")
  }, error = function(e) {
    message("Error in main process: ", e$message)
    stop(e)
  })
}

# Run main function
main()

# Close logging
sink(type = "message")
sink()
close(log_file) 