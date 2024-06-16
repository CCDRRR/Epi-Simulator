# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 17:34:28 2024

@author: alext
"""

import argparse
import pandas as pd
import os
import matplotlib.pyplot as plt
from Environment import SIERDModel

def run_simulation(width, height, density, transmission_rate, latency_period, infection_duration, recovery_rate, policy, num_districts, initial_infected, steps):
    model = SIERDModel(width, height, density, transmission_rate, latency_period, infection_duration, recovery_rate, policy, num_districts, initial_infected)
    for _ in range(steps):
        model.step()
    results = model.datacollector.get_model_vars_dataframe()
    return results

def save_results(results, filename):
    results.to_csv(filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, default=10, help="Width of the grid")
    parser.add_argument("--height", type=int, default=10, help="Height of the grid")
    parser.add_argument("--density", type=float, default=0.9, help="Density of the agents")
    parser.add_argument("--transmission_rate", type=float, default=0.6, help="Transmission rate of the virus")
    parser.add_argument("--latency_period", type=int, default=15, help="Latency period of the virus")
    parser.add_argument("--infection_duration", type=int, default=50, help="Infection duration of the virus")
    parser.add_argument("--recovery_rate", type=float, default=0.3, help="Recovery rate from the virus")
    parser.add_argument("--num_districts", type=int, default=5, help="Number of districts in the environment")
    parser.add_argument("--initial_infected", type=int, default=50, help="Number of initially infected agents")
    parser.add_argument("--steps", type=int, default=500, help="Number of steps to simulate")
    parser.add_argument("--output_dir", type=str, default="results", help="Output directory to save the results")
    args = parser.parse_args()

    # Define policies
    policies = ["No Interventions", "Lockdown Only", "Mask Policy Only", "Combination of Lockdown and Mask Policy"]

    # Ensure the output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Run model for each policy
    for policy in policies:
        print(f"Running model with policy: {policy}")
        results = run_simulation(args.width, args.height, args.density, args.transmission_rate, args.latency_period, args.infection_duration, args.recovery_rate, policy, args.num_districts, args.initial_infected, args.steps)
        
        # Save results to CSV
        csv_filename = f"{args.output_dir}/results_{policy.replace(' ', '_').lower()}.csv"
        save_results(results, csv_filename)
        print(f"Results saved to {csv_filename}")

        # Data analysis
        results.plot(title=f"Policy: {policy}")
        plt.show()