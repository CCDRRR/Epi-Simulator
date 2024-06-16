# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 17:34:28 2024

@author: alext
"""

import argparse
import matplotlib.pyplot as plt
from Environment import SIERDModel

def main(args):
    # Parameters from command line arguments
    width = args.width
    height = args.height
    density = args.density
    transmission_rate = args.transmission_rate
    latency_period = args.latency_period
    infection_duration = args.infection_duration
    recovery_rate = args.recovery_rate
    initial_infected = args.initial_infected
    policies = args.policies.split(',')
    steps = args.steps
    output_dir = args.output_dir

    # Run model for each policy
    for policy in policies:
        print(f"Running model with policy: {policy}")
        model = SIERDModel(width, height, density, transmission_rate, latency_period, infection_duration, recovery_rate, policy, initial_infected)
        for i in range(steps):
            model.step()

        # Save results to CSV
        csv_filename = f"{output_dir}/results_{policy.replace(' ', '_').lower()}.csv"
        model.save_results_to_csv(csv_filename)
        print(f"Results saved to {csv_filename}")

        # Data analysis
        results = model.get_results_dataframe()
        results.plot(title=f"Policy: {policy}")
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SIERD Model with different policies.")
    parser.add_argument("--width", type=int, default=50, help="Width of the grid.")
    parser.add_argument("--height", type=int, default=50, help="Height of the grid.")
    parser.add_argument("--density", type=float, default=0.1, help="Density of the agents in the grid.")
    parser.add_argument("--transmission_rate", type=float, default=0.2, help="Probability of transmission per contact.")
    parser.add_argument("--latency_period", type=int, default=3, help="Number of steps an agent stays in the exposed state.")
    parser.add_argument("--infection_duration", type=int, default=14, help="Number of steps an agent stays in the infected state.")
    parser.add_argument("--recovery_rate", type=float, default=0.95, help="Probability of recovering from the infected state.")
    parser.add_argument("--initial_infected", type=int, default=10, help="Initial number of infected agents.")
    parser.add_argument("--policies", type=str, default="No Interventions,Lockdown Only,Mask Policy Only,Combination of Lockdown and Mask Policy", help="Comma-separated list of policies to run.")
    parser.add_argument("--steps", type=int, default=100, help="Number of steps to run the model.")
    parser.add_argument("--output_dir", type=str, default=".", help="Directory to save the CSV files.")

    args = parser.parse_args()
    main(args)