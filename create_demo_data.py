#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo Data Generator for Airline No-Show Prediction
Creates realistic sample data for demonstration purposes
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_demo_data(n_samples=1000):
    """Generate realistic airline booking data for demo purposes."""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Define realistic parameters
    routes = [
        'NYC-LON', 'LAX-MIA', 'CHI-DEN', 'SFO-LAX', 'BOS-DCA',
        'SEA-PDX', 'ATL-DFW', 'PHX-LAS', 'ORD-MIA', 'JFK-SFO',
        'DFW-LAX', 'DEN-SEA', 'MIA-ATL', 'LAS-PHX', 'BWI-ORD'
    ]
    
    fare_classes = ['Economy', 'Business', 'First']
    customer_types = ['Business', 'Leisure']
    
    # Generate base data
    data = []
    
    for i in range(n_samples):
        # Random booking date (last 6 months)
        booking_date = datetime.now() - timedelta(days=random.randint(1, 180))
        
        # Lead time (1-90 days, with some patterns)
        if random.random() < 0.3:  # 30% are last-minute bookings
            lead_time = random.randint(1, 7)
        elif random.random() < 0.7:  # 40% are normal bookings
            lead_time = random.randint(8, 30)
        else:  # 30% are advance bookings
            lead_time = random.randint(31, 90)
        
        flight_date = booking_date + timedelta(days=lead_time)
        
        # Route selection (some routes more popular)
        route = random.choices(routes, weights=[10, 8, 6, 5, 4, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1])[0]
        
        # Fare class (economy most common)
        fare_class = random.choices(fare_classes, weights=[70, 25, 5])[0]
        
        # Customer type
        customer_type = random.choices(customer_types, weights=[40, 60])[0]
        
        # Generate realistic no-show probability based on features
        base_prob = 0.15  # Base 15% no-show rate
        
        # Adjust based on fare class
        if fare_class == 'First':
            base_prob *= 0.3  # First class rarely no-show
        elif fare_class == 'Business':
            base_prob *= 0.6  # Business class less likely to no-show
        else:  # Economy
            base_prob *= 1.2  # Economy more likely to no-show
        
        # Adjust based on customer type
        if customer_type == 'Business':
            base_prob *= 0.7  # Business travelers more reliable
        else:  # Leisure
            base_prob *= 1.3  # Leisure travelers more likely to no-show
        
        # Adjust based on lead time
        if lead_time <= 7:
            base_prob *= 1.5  # Last-minute bookings more likely to no-show
        elif lead_time <= 30:
            base_prob *= 1.0  # Normal bookings
        else:
            base_prob *= 0.8  # Advance bookings less likely to no-show
        
        # Adjust based on route (some routes have higher no-show rates)
        if route in ['NYC-LON', 'LAX-MIA', 'CHI-DEN']:
            base_prob *= 1.1  # Popular routes
        elif route in ['SEA-PDX', 'ATL-DFW']:
            base_prob *= 0.9  # Business routes
        
        # Add some randomness
        base_prob *= random.uniform(0.8, 1.2)
        
        # Ensure probability is between 0.01 and 0.95
        no_show_prob = max(0.01, min(0.95, base_prob))
        
        # Determine actual no-show (1 or 0)
        no_show = 1 if random.random() < no_show_prob else 0
        
        # Create record
        record = {
            'booking_date': booking_date.strftime('%Y-%m-%d'),
            'flight_date': flight_date.strftime('%Y-%m-%d'),
            'route': route,
            'fare_class': fare_class,
            'customer_type': customer_type,
            'lead_time': lead_time,
            'no_show_probability': round(no_show_prob, 3),
            'no_show': no_show
        }
        
        data.append(record)
    
    return pd.DataFrame(data)

def create_demo_scenarios():
    """Create specific demo scenarios for presentation."""
    
    scenarios = [
        {
            'name': 'High-Value Business Traveler',
            'booking_date': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
            'flight_date': datetime.now().strftime('%Y-%m-%d'),
            'route': 'NYC-LON',
            'fare_class': 'Business',
            'customer_type': 'Business',
            'lead_time': 2,
            'expected_risk': 'Low',
            'description': 'Premium business traveler with short lead time'
        },
        {
            'name': 'Budget Leisure Traveler',
            'booking_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'flight_date': (datetime.now() + timedelta(days=28)).strftime('%Y-%m-%d'),
            'route': 'LAX-MIA',
            'fare_class': 'Economy',
            'customer_type': 'Leisure',
            'lead_time': 30,
            'expected_risk': 'Medium',
            'description': 'Leisure traveler with advance booking'
        },
        {
            'name': 'Last-Minute Leisure Booking',
            'booking_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
            'flight_date': datetime.now().strftime('%Y-%m-%d'),
            'route': 'CHI-DEN',
            'fare_class': 'Economy',
            'customer_type': 'Leisure',
            'lead_time': 1,
            'expected_risk': 'High',
            'description': 'Last-minute leisure booking with high no-show risk'
        },
        {
            'name': 'Premium First Class',
            'booking_date': (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d'),
            'flight_date': (datetime.now() + timedelta(days=12)).strftime('%Y-%m-%d'),
            'route': 'JFK-SFO',
            'fare_class': 'First',
            'customer_type': 'Business',
            'lead_time': 14,
            'expected_risk': 'Low',
            'description': 'First class business traveler'
        },
        {
            'name': 'Seasonal Leisure Travel',
            'booking_date': (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d'),
            'flight_date': (datetime.now() + timedelta(days=58)).strftime('%Y-%m-%d'),
            'route': 'SFO-LAX',
            'fare_class': 'Economy',
            'customer_type': 'Leisure',
            'lead_time': 60,
            'expected_risk': 'Medium',
            'description': 'Long-term leisure booking'
        }
    ]
    
    return scenarios

def main():
    """Generate demo data and scenarios."""
    
    print("Generating demo data for Airline No-Show Prediction...")
    
    # Create directories if they don't exist
    os.makedirs('data/demo', exist_ok=True)
    os.makedirs('demo_scenarios', exist_ok=True)
    
    # Generate main dataset
    print("Creating sample dataset...")
    demo_data = generate_demo_data(1000)
    demo_data.to_csv('data/demo/sample_airline_data.csv', index=False)
    print(f"Generated {len(demo_data)} sample records")
    
    # Generate demo scenarios
    print("Creating demo scenarios...")
    scenarios = create_demo_scenarios()
    
    # Save scenarios as CSV
    scenarios_df = pd.DataFrame(scenarios)
    scenarios_df.to_csv('demo_scenarios/demo_scenarios.csv', index=False)
    
    # Create a markdown file with scenarios
    with open('demo_scenarios/README.md', 'w') as f:
        f.write("# Demo Scenarios for Airline No-Show Prediction\n\n")
        f.write("Use these scenarios to demonstrate the system:\n\n")
        
        for i, scenario in enumerate(scenarios, 1):
            f.write(f"## Scenario {i}: {scenario['name']}\n")
            f.write(f"**Description**: {scenario['description']}\n\n")
            f.write("**Input Parameters**:\n")
            f.write(f"- Booking Date: {scenario['booking_date']}\n")
            f.write(f"- Flight Date: {scenario['flight_date']}\n")
            f.write(f"- Route: {scenario['route']}\n")
            f.write(f"- Fare Class: {scenario['fare_class']}\n")
            f.write(f"- Customer Type: {scenario['customer_type']}\n")
            f.write(f"- Lead Time: {scenario['lead_time']} days\n")
            f.write(f"- Expected Risk: {scenario['expected_risk']}\n\n")
            f.write("**Demo Talking Points**:\n")
            if scenario['expected_risk'] == 'Low':
                f.write("- This represents a reliable business traveler\n")
                f.write("- Short lead time but premium fare class\n")
                f.write("- Expected no-show probability: 10-20%\n\n")
            elif scenario['expected_risk'] == 'Medium':
                f.write("- This represents a typical leisure traveler\n")
                f.write("- Advance booking but economy class\n")
                f.write("- Expected no-show probability: 25-40%\n\n")
            else:  # High risk
                f.write("- This represents a high-risk booking\n")
                f.write("- Last-minute booking with leisure travel\n")
                f.write("- Expected no-show probability: 50-70%\n\n")
    
    # Generate summary statistics
    print("\nGenerating summary statistics...")
    summary_stats = {
        'total_bookings': len(demo_data),
        'no_show_rate': demo_data['no_show'].mean(),
        'avg_lead_time': demo_data['lead_time'].mean(),
        'fare_class_distribution': demo_data['fare_class'].value_counts().to_dict(),
        'customer_type_distribution': demo_data['customer_type'].value_counts().to_dict(),
        'route_distribution': demo_data['route'].value_counts().head(10).to_dict()
    }
    
    # Save summary statistics
    with open('data/demo/summary_stats.txt', 'w') as f:
        f.write("Demo Data Summary Statistics\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Total Bookings: {summary_stats['total_bookings']:,}\n")
        f.write(f"Overall No-Show Rate: {summary_stats['no_show_rate']:.1%}\n")
        f.write(f"Average Lead Time: {summary_stats['avg_lead_time']:.1f} days\n\n")
        
        f.write("Fare Class Distribution:\n")
        for fare_class, count in summary_stats['fare_class_distribution'].items():
            f.write(f"  {fare_class}: {count:,} ({count/len(demo_data)*100:.1f}%)\n")
        
        f.write("\nCustomer Type Distribution:\n")
        for customer_type, count in summary_stats['customer_type_distribution'].items():
            f.write(f"  {customer_type}: {count:,} ({count/len(demo_data)*100:.1f}%)\n")
        
        f.write("\nTop Routes:\n")
        for route, count in summary_stats['route_distribution'].items():
            f.write(f"  {route}: {count:,} bookings\n")
    
    print("Demo data generation completed!")
    print(f"Files created:")
    print(f"- data/demo/sample_airline_data.csv")
    print(f"- demo_scenarios/demo_scenarios.csv")
    print(f"- demo_scenarios/README.md")
    print(f"- data/demo/summary_stats.txt")
    
    print(f"\nSummary:")
    print(f"- Total bookings: {len(demo_data):,}")
    print(f"- No-show rate: {demo_data['no_show'].mean():.1%}")
    print(f"- Average lead time: {demo_data['lead_time'].mean():.1f} days")
    print(f"- Demo scenarios: {len(scenarios)}")

if __name__ == "__main__":
    main()


