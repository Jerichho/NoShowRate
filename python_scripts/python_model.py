#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modeling Script for Airline No-Show Prediction
Author: [Your Name]
Date: [Current Date]

This script implements various machine learning models to predict airline no-show rates.
It includes logistic regression, random forest, and other models for comparison.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                           f1_score, roc_auc_score, confusion_matrix)
import joblib
import logging
import os
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('modeling.log'),
        logging.StreamHandler()
    ]
)

def setup_directories():
    """Create necessary directories if they don't exist."""
    directories = ['../models', '../outputs/model_metrics']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def load_data(file_path):
    """
    Load the cleaned data file.
    
    Args:
        file_path (str): Path to the cleaned data file
        
    Returns:
        pandas.DataFrame: Loaded data
    """
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Successfully loaded data from {file_path}")
        return df
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
        raise

def prepare_data(df, target_col='no_show', test_size=0.2, random_state=42):
    """
    Prepare data for modeling by splitting into features and target,
    and then into training and test sets.
    Excludes non-numeric columns (e.g., dates).
    
    Args:
        df (pandas.DataFrame): Input dataframe
        target_col (str): Name of the target column
        test_size (float): Proportion of data to use for testing
        random_state (int): Random seed for reproducibility
        
    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    # Drop non-numeric columns (e.g., dates, IDs)
    drop_cols = [target_col]
    for col in df.columns:
        if df[col].dtype == 'object' and col not in drop_cols:
            drop_cols.append(col)
    X = df.drop(columns=drop_cols)
    y = df[target_col]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save scaler
    joblib.dump(scaler, '../models/scaler.joblib')
    
    return X_train_scaled, X_test_scaled, y_train, y_test

def train_logistic_regression(X_train, y_train, random_state=42):
    """
    Train a logistic regression model.
    
    Args:
        X_train: Training features
        y_train: Training target
        random_state (int): Random seed for reproducibility
        
    Returns:
        sklearn.linear_model.LogisticRegression: Trained model
    """
    model = LogisticRegression(random_state=random_state, max_iter=1000)
    model.fit(X_train, y_train)
    
    # Save model
    joblib.dump(model, '../models/logistic_regression.joblib')
    
    return model

def train_random_forest(X_train, y_train, random_state=42):
    """
    Train a random forest model.
    
    Args:
        X_train: Training features
        y_train: Training target
        random_state (int): Random seed for reproducibility
        
    Returns:
        sklearn.ensemble.RandomForestClassifier: Trained model
    """
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=random_state
    )
    model.fit(X_train, y_train)
    
    # Save model
    joblib.dump(model, '../models/random_forest.joblib')
    
    return model

def evaluate_model(model, X_test, y_test, model_name):
    """
    Evaluate a model using various metrics.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test target
        model_name (str): Name of the model for logging
        
    Returns:
        dict: Dictionary of evaluation metrics
    """
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_pred_proba)
    }
    
    # Log metrics
    logging.info(f"\nMetrics for {model_name}:")
    for metric, value in metrics.items():
        logging.info(f"{metric}: {value:.4f}")
    
    # Save confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    cm_df = pd.DataFrame(
        cm,
        index=['Actual No-Show', 'Actual Show'],
        columns=['Predicted No-Show', 'Predicted Show']
    )
    cm_df.to_csv(f'../outputs/model_metrics/{model_name}_confusion_matrix.csv')
    
    return metrics

def main():
    """Main function to orchestrate the modeling process."""
    try:
        # Setup directories
        setup_directories()
        
        # Load data
        data_path = 'data/processed/cleaned_data.csv'
        df = load_data(data_path)
        
        # Prepare data
        X_train, X_test, y_train, y_test = prepare_data(df)
        
        # Train and evaluate models
        models = {
            'logistic_regression': train_logistic_regression(X_train, y_train),
            'random_forest': train_random_forest(X_train, y_train)
        }
        
        # Evaluate all models
        results = {}
        for name, model in models.items():
            results[name] = evaluate_model(model, X_test, y_test, name)
        
        # Save results
        results_df = pd.DataFrame(results).T
        results_df.to_csv('../outputs/model_metrics/model_comparison.csv')
        
        logging.info("Modeling completed successfully")
        
    except Exception as e:
        logging.error(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main() 