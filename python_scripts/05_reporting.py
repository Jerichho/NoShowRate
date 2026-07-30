#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reporting Script for Airline No-Show Prediction
Author: [Your Name]
Date: [Current Date]

This script generates a comprehensive report and dashboard for the airline no-show prediction project.
It includes visualizations, model performance metrics, and business insights.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import logging
import os
import json
from jinja2 import Template
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reporting.log'),
        logging.StreamHandler()
    ]
)

def setup_directories():
    """Create necessary directories if they don't exist."""
    directories = ['outputs/reports', 'outputs/dashboard']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def load_metrics():
    """
    Load model performance metrics from the CSV file.
    
    Returns:
        pandas.DataFrame: Loaded metrics
    """
    try:
        metrics = pd.read_csv('outputs/model_metrics/model_comparison.csv')
        logging.info("Successfully loaded metrics from model_comparison.csv")
        return metrics
    except Exception as e:
        logging.error(f"Error loading metrics: {str(e)}")
        raise

def load_business_impact():
    """
    Load business impact analysis. If the file is not available, return a placeholder DataFrame.
    
    Returns:
        pandas.DataFrame: Business impact metrics or placeholder
    """
    try:
        impact = pd.read_csv('outputs/model_metrics/business_impact.csv')
        logging.info("Successfully loaded business impact analysis")
        return impact
    except FileNotFoundError:
        logging.warning("Business impact file not found. Using placeholder data.")
        # Placeholder data
        impact = pd.DataFrame({
            'Model': ['logistic_regression', 'random_forest'],
            'Total_Cost': [0, 0],
            'Cost_Per_Prediction': [0, 0]
        })
        return impact
    except Exception as e:
        logging.error(f"Error loading business impact: {str(e)}")
        raise

def create_performance_dashboard(metrics):
    """
    Create an interactive dashboard for model performance metrics.
    
    Args:
        metrics (pandas.DataFrame): Model performance metrics
    """
    # Get absolute paths
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    dashboard_path = os.path.join(base_dir, 'outputs', 'dashboard')
    reports_path = os.path.join(base_dir, 'outputs', 'reports')
    
    # Reset index to use model names
    metrics = metrics.reset_index().rename(columns={'index': 'Model'})
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Accuracy and F1 Score', 'Precision and Recall',
                       'ROC AUC', 'Business Impact')
    )
    
    # Add bar charts
    fig.add_trace(
        go.Bar(name='Accuracy', x=metrics['Model'], y=metrics['accuracy']),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(name='F1 Score', x=metrics['Model'], y=metrics['f1']),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(name='Precision', x=metrics['Model'], y=metrics['precision']),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(name='Recall', x=metrics['Model'], y=metrics['recall']),
        row=1, col=2
    )
    
    # Add ROC AUC
    fig.add_trace(
        go.Bar(name='ROC AUC', x=metrics['Model'], y=metrics['roc_auc']),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title_text='Model Performance Dashboard',
        height=800,
        showlegend=True
    )
    
    # Add navigation buttons
    html_content = fig.to_html(full_html=True, include_plotlyjs=True)
    nav_buttons = f"""
    <div style="position: fixed; top: 20px; right: 20px; display: flex; gap: 10px;">
        <a href="file://{reports_path}/final_report.html" style="padding: 10px 20px; background-color: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; font-weight: bold;">View Final Report</a>
        <a href="file://{dashboard_path}/business_impact.html" style="padding: 10px 20px; background-color: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; font-weight: bold;">View Business Impact</a>
    </div>
    """
    html_content = html_content.replace('</body>', f'{nav_buttons}</body>')
    
    # Save dashboard
    with open(os.path.join(dashboard_path, 'performance_dashboard.html'), 'w') as f:
        f.write(html_content)
    logging.info("Saved performance dashboard")

def create_business_insights(impact):
    """
    Create business insights visualization.
    
    Args:
        impact (pandas.DataFrame): Business impact metrics
    """
    # Get absolute paths
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    dashboard_path = os.path.join(base_dir, 'outputs', 'dashboard')
    reports_path = os.path.join(base_dir, 'outputs', 'reports')
    
    # Create cost comparison plot
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Total Cost',
        x=impact['Model'],
        y=impact['Total_Cost']
    ))
    
    fig.add_trace(go.Bar(
        name='Cost Per Prediction',
        x=impact['Model'],
        y=impact['Cost_Per_Prediction']
    ))
    
    fig.update_layout(
        title='Business Impact Analysis',
        xaxis_title='Model',
        yaxis_title='Cost',
        barmode='group'
    )
    
    # Add navigation buttons
    html_content = fig.to_html(full_html=True, include_plotlyjs=True)
    nav_buttons = f"""
    <div style="position: fixed; top: 20px; right: 20px; display: flex; gap: 10px;">
        <a href="file://{reports_path}/final_report.html" style="padding: 10px 20px; background-color: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; font-weight: bold;">View Final Report</a>
        <a href="file://{dashboard_path}/performance_dashboard.html" style="padding: 10px 20px; background-color: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; font-weight: bold;">View Performance Dashboard</a>
    </div>
    """
    html_content = html_content.replace('</body>', f'{nav_buttons}</body>')
    
    # Save plot
    with open(os.path.join(dashboard_path, 'business_impact.html'), 'w') as f:
        f.write(html_content)
    logging.info("Saved business impact visualization")

def generate_html_report(metrics, impact):
    """
    Generate an HTML report with all findings.
    
    Args:
        metrics (pandas.DataFrame): Model performance metrics
        impact (pandas.DataFrame): Business impact metrics
    """
    # Get absolute paths
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    dashboard_path = os.path.join(base_dir, 'outputs', 'dashboard')
    reports_path = os.path.join(base_dir, 'outputs', 'reports')
    
    # Load HTML template
    template_str = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Airline No-Show Prediction Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #2c3e50; }
            h2 { color: #34495e; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .metric { margin: 20px 0; }
            .nav-buttons {
                position: fixed;
                top: 20px;
                right: 20px;
                display: flex;
                gap: 10px;
            }
            .nav-button {
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                font-weight: bold;
            }
            .nav-button:hover {
                background-color: #2980b9;
            }
        </style>
    </head>
    <body>
        <div class="nav-buttons">
            <a href="file://{{ dashboard_path }}/performance_dashboard.html" class="nav-button">View Performance Dashboard</a>
            <a href="file://{{ dashboard_path }}/business_impact.html" class="nav-button">View Business Impact</a>
        </div>
        
        <h1>Airline No-Show Prediction Report</h1>
        <p>Generated on: {{ timestamp }}</p>
        
        <h2>Model Performance Metrics</h2>
        {{ metrics_table }}
        
        <h2>Business Impact Analysis</h2>
        {{ impact_table }}
        
        <h2>Key Findings</h2>
        <ul>
            <li>Best performing model: {{ best_model }}</li>
            <li>Cost savings potential: ${{ cost_savings }}</li>
            <li>Recommended actions: {{ recommendations }}</li>
        </ul>
        
        <h2>Visualizations</h2>
        <p>Use the navigation buttons in the top-right corner to view interactive visualizations.</p>
    </body>
    </html>
    """
    
    # Create template
    template = Template(template_str)
    
    # Prepare data for template
    best_model = metrics.index[metrics['f1'].idxmax()]
    cost_savings = impact['Total_Cost'].min()
    recommendations = [
        "Implement the best performing model for no-show prediction",
        "Adjust overbooking strategies based on predicted no-show rates",
        "Monitor model performance regularly and retrain as needed"
    ]
    
    # Render template
    html_content = template.render(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        metrics_table=metrics.to_html(),
        impact_table=impact.to_html(),
        best_model=best_model,
        cost_savings=cost_savings,
        recommendations="<br>".join(recommendations),
        dashboard_path=dashboard_path
    )
    
    # Save report
    with open(os.path.join(reports_path, 'final_report.html'), 'w') as f:
        f.write(html_content)
    logging.info("Generated HTML report")

def main():
    """Main function to orchestrate the reporting process."""
    try:
        # Setup directories
        setup_directories()
        
        # Load data
        metrics = load_metrics()
        impact = load_business_impact()
        
        # Create visualizations
        create_performance_dashboard(metrics)
        create_business_insights(impact)
        
        # Generate report
        generate_html_report(metrics, impact)
        
        logging.info("Reporting completed successfully")
        
    except Exception as e:
        logging.error(f"Error in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main() 