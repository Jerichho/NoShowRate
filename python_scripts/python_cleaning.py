#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data Cleaning Script for Airline No-Show Prediction
Author: [Your Name]
Date: [Current Date]

This script handles the data cleaning and preprocessing steps for the airline no-show prediction project.
It includes handling missing values, standardizing date formats, and encoding categorical variables.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_cleaning.log'),
        logging.StreamHandler()
    ]
)

def setup_directories():
    """Create necessary directories if they don't exist."""
    directories = ['../data/processed', '../data/interim']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def load_data(file_path):
    """
    Load the raw data file.
    
    Args:
        file_path (str): Path to the raw data file
        
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

def standardize_dates(df, date_columns):
    """
    Standardize date formats to ISO 8601 (YYYY-MM-DD).
    
    Args:
        df (pandas.DataFrame): Input dataframe
        date_columns (list): List of column names containing dates
        
    Returns:
        pandas.DataFrame: DataFrame with standardized dates
    """
    for col in date_columns:
        try:
            df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
            logging.info(f"Standardized date format for column: {col}")
        except Exception as e:
            logging.warning(f"Could not standardize dates for column {col}: {str(e)}")
    return df

def handle_missing_values(df, strategy='mean'):
    """
    Handle missing values in the dataset.
    
    Args:
        df (pandas.DataFrame): Input dataframe
        strategy (str): Strategy for handling missing values ('mean', 'median', 'mode')
        
    Returns:
        pandas.DataFrame: DataFrame with handled missing values
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    for col in numeric_cols:
        if df[col].isnull().any():
            if strategy == 'mean':
                df[col].fillna(df[col].mean(), inplace=True)
            elif strategy == 'median':
                df[col].fillna(df[col].median(), inplace=True)
            logging.info(f"Filled missing values in {col} using {strategy}")
    
    for col in categorical_cols:
        if df[col].isnull().any():
            df[col].fillna(df[col].mode()[0], inplace=True)
            logging.info(f"Filled missing values in {col} using mode")
    
    return df

def encode_categorical_variables(df, categorical_columns):
    """
    Encode categorical variables using one-hot encoding.
    
    Args:
        df (pandas.DataFrame): Input dataframe
        categorical_columns (list): List of categorical column names
        
    Returns:
        pandas.DataFrame: DataFrame with encoded categorical variables
    """
    df_encoded = pd.get_dummies(df, columns=categorical_columns, prefix=categorical_columns)
    logging.info(f"Encoded categorical variables: {categorical_columns}")
    return df_encoded

def main():
    """Main function to orchestrate the data cleaning process."""
    try:
        # Setup directories
        setup_directories()
        
        # Load data
        raw_data_path = 'data/raw/airline_data.csv'  # Updated path
        df = load_data(raw_data_path)
        
        # Define date columns (update based on your data)
        date_columns = ['booking_date', 'flight_date']
        
        # Standardize dates
        df = standardize_dates(df, date_columns)
        
        # Handle missing values
        df = handle_missing_values(df, strategy='mean')
        
        # Define categorical columns (update based on your data)
        categorical_columns = ['fare_class', 'route', 'customer_type']
        
        # Encode categorical variables
        df = encode_categorical_variables(df, categorical_columns)
        
        # Save processed data
        cleaned_data_path = 'data/processed/cleaned_data.csv'  # Updated path
        df.to_csv(cleaned_data_path, index=False)
        logging.info(f"Saved cleaned data to {cleaned_data_path}")
        
        logging.info("Data cleaning completed successfully")
        
    except Exception as e:
        logging.error(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main() 