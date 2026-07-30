#!/usr/bin/env Rscript

# Model Evaluation Script for Airline No-Show Prediction
# Author: [Your Name]
# Date: [Current Date]

# Load required libraries
library(tidyverse)
library(caret)
library(pROC)
library(ggplot2)
library(gridExtra)

# Set up logging
log_file <- file("evaluation.log")
sink(log_file, append = TRUE)
sink(log_file, append = TRUE, type = "message")

# Function to load model results
load_model_results <- function(file_path) {
  tryCatch({
    results <- read.csv(file_path)
    message("Successfully loaded model results from ", file_path)
    return(results)
  }, error = function(e) {
    message("Error loading model results: ", e$message)
    stop(e)
  })
}

# Function to create ROC curves
plot_roc_curves <- function(results_list, model_names) {
  # Create ROC curve for each model
  roc_curves <- list()
  for (i in seq_along(results_list)) {
    roc_obj <- roc(results_list[[i]]$actual, results_list[[i]]$predicted_prob)
    roc_curves[[i]] <- data.frame(
      FPR = 1 - roc_obj$specificities,
      TPR = roc_obj$sensitivities,
      Model = model_names[i]
    )
  }
  
  # Combine all curves
  all_curves <- do.call(rbind, roc_curves)
  
  # Create plot
  p <- ggplot(all_curves, aes(x = FPR, y = TPR, color = Model)) +
    geom_line() +
    geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "gray") +
    labs(title = "ROC Curves Comparison",
         x = "False Positive Rate",
         y = "True Positive Rate") +
    theme_minimal()
  
  # Save plot
  ggsave("../outputs/model_metrics/roc_curves.png", p, width = 10, height = 6)
  message("Saved ROC curves plot")
}

# Function to create feature importance plot
plot_feature_importance <- function(importance_data, model_name) {
  p <- ggplot(importance_data, aes(x = reorder(Feature, Importance), y = Importance)) +
    geom_bar(stat = "identity", fill = "steelblue") +
    coord_flip() +
    labs(title = paste("Feature Importance -", model_name),
         x = "Features",
         y = "Importance") +
    theme_minimal()
  
  # Save plot
  ggsave(paste0("../outputs/model_metrics/", model_name, "_feature_importance.png"),
         p, width = 10, height = 6)
  message(paste("Saved feature importance plot for", model_name))
}

# Function to create confusion matrix heatmap
plot_confusion_matrix <- function(cm_data, model_name) {
  p <- ggplot(cm_data, aes(x = Predicted, y = Actual, fill = Count)) +
    geom_tile() +
    scale_fill_gradient(low = "white", high = "steelblue") +
    geom_text(aes(label = Count), color = "black") +
    labs(title = paste("Confusion Matrix -", model_name)) +
    theme_minimal()
  
  # Save plot
  ggsave(paste0("../outputs/model_metrics/", model_name, "_confusion_matrix.png"),
         p, width = 8, height = 6)
  message(paste("Saved confusion matrix plot for", model_name))
}

# Function to create performance metrics table
create_metrics_table <- function(results_list, model_names) {
  metrics <- data.frame(
    Model = model_names,
    Accuracy = sapply(results_list, function(x) mean(x$actual == x$predicted)),
    Precision = sapply(results_list, function(x) {
      cm <- confusionMatrix(factor(x$predicted), factor(x$actual))
      cm$byClass["Precision"]
    }),
    Recall = sapply(results_list, function(x) {
      cm <- confusionMatrix(factor(x$predicted), factor(x$actual))
      cm$byClass["Recall"]
    }),
    F1_Score = sapply(results_list, function(x) {
      cm <- confusionMatrix(factor(x$predicted), factor(x$actual))
      cm$byClass["F1"]
    }),
    AUC = sapply(results_list, function(x) {
      roc_obj <- roc(x$actual, x$predicted_prob)
      auc(roc_obj)
    })
  )
  
  # Save metrics
  write.csv(metrics, "../outputs/model_metrics/performance_metrics.csv", row.names = FALSE)
  message("Saved performance metrics table")
  
  return(metrics)
}

# Function to create business impact analysis
analyze_business_impact <- function(results_list, model_names, cost_matrix) {
  impact <- data.frame(
    Model = model_names,
    Total_Cost = sapply(results_list, function(x) {
      cm <- confusionMatrix(factor(x$predicted), factor(x$actual))
      sum(cm$table * cost_matrix)
    }),
    Cost_Per_Prediction = sapply(results_list, function(x) {
      cm <- confusionMatrix(factor(x$predicted), factor(x$actual))
      sum(cm$table * cost_matrix) / length(x$actual)
    })
  )
  
  # Save impact analysis
  write.csv(impact, "../outputs/model_metrics/business_impact.csv", row.names = FALSE)
  message("Saved business impact analysis")
  
  return(impact)
}

# Main function
main <- function() {
  tryCatch({
    # Create output directory if it doesn't exist
    dir.create("../outputs/model_metrics", showWarnings = FALSE, recursive = TRUE)
    
    # Load model results
    results_files <- list.files("../outputs/model_metrics", pattern = "*_results.csv", full.names = TRUE)
    results_list <- lapply(results_files, load_model_results)
    model_names <- gsub(".*/(.*)_results.csv", "\\1", results_files)
    
    # Create visualizations
    plot_roc_curves(results_list, model_names)
    
    # Load and plot feature importance
    importance_files <- list.files("../outputs/model_metrics", pattern = "*_importance.csv", full.names = TRUE)
    for (i in seq_along(importance_files)) {
      importance_data <- read.csv(importance_files[i])
      plot_feature_importance(importance_data, model_names[i])
    }
    
    # Load and plot confusion matrices
    cm_files <- list.files("../outputs/model_metrics", pattern = "*_confusion_matrix.csv", full.names = TRUE)
    for (i in seq_along(cm_files)) {
      cm_data <- read.csv(cm_files[i])
      plot_confusion_matrix(cm_data, model_names[i])
    }
    
    # Create performance metrics table
    metrics <- create_metrics_table(results_list, model_names)
    
    # Define cost matrix for business impact analysis
    cost_matrix <- matrix(c(
      0, 100,  # Cost of true negative, false positive
      500, 0   # Cost of false negative, true positive
    ), nrow = 2)
    
    # Analyze business impact
    impact <- analyze_business_impact(results_list, model_names, cost_matrix)
    
    message("Evaluation completed successfully")
    
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