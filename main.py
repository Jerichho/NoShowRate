#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main Program for Airline No-Show Prediction
This script orchestrates the entire process from data cleaning to report generation.
"""

import os
import sys
import subprocess
import webbrowser
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log'),
        logging.StreamHandler()
    ]
)

def setup_environment():
    """Set up the required environment and directories."""
    try:
        # Create necessary directories
        directories = [
            'data/raw',
            'data/processed',
            'outputs/dashboard',
            'outputs/model_metrics',
            'outputs/reports'
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        # Install required packages
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        logging.info("Environment setup completed")
    except Exception as e:
        logging.error(f"Error setting up environment: {str(e)}")
        raise

def run_script(script_path):
    """Run a Python script and handle any errors."""
    try:
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        if result.returncode != 0:
            logging.error(f"Error running {script_path}: {result.stderr}")
            raise Exception(f"Script {script_path} failed")
        logging.info(f"Successfully ran {script_path}")
    except Exception as e:
        logging.error(f"Error running {script_path}: {str(e)}")
        raise

def open_results():
    """Open the generated reports and visualizations in the default web browser."""
    try:
        # Open the final report
        report_path = os.path.abspath('outputs/reports/final_report.html')
        webbrowser.open(f'file://{report_path}')
        logging.info("Opened final report")
        
        # Open the performance dashboard
        dashboard_path = os.path.abspath('outputs/dashboard/performance_dashboard.html')
        webbrowser.open(f'file://{dashboard_path}')
        logging.info("Opened performance dashboard")
        
        # Open the business impact visualization
        impact_path = os.path.abspath('outputs/dashboard/business_impact.html')
        webbrowser.open(f'file://{impact_path}')
        logging.info("Opened business impact visualization")
    except Exception as e:
        logging.error(f"Error opening results: {str(e)}")
        raise

def main():
    """Main function to orchestrate the entire process."""
    try:
        print("Starting Airline No-Show Prediction Program...")
        print("=" * 50)
        
        # Step 1: Set up environment
        print("\n1. Setting up environment...")
        setup_environment()
        
        # Step 2: Run data cleaning
        print("\n2. Running data cleaning...")
        run_script('python_scripts/python_cleaning.py')
        
        # Step 3: Run modeling
        print("\n3. Running modeling...")
        run_script('python_scripts/python_model.py')
        
        # Step 4: Generate reports
        print("\n4. Generating reports...")
        run_script('python_scripts/05_reporting.py')
        
        # Step 5: Open results
        print("\n5. Opening results...")
        open_results()
        
        print("\nProgram completed successfully!")
        print("=" * 50)
        print("\nResults have been opened in your web browser.")
        print("You can find the following files:")
        print("- Final Report: outputs/reports/final_report.html")
        print("- Performance Dashboard: outputs/dashboard/performance_dashboard.html")
        print("- Business Impact: outputs/dashboard/business_impact.html")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please check the main.log file for details.")
        sys.exit(1)

if __name__ == "__main__":
    main() 