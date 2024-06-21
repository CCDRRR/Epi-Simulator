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

def run_simulation(width, height, density, transmission_rate, latency_period, infection_duration, recovery_rate, policy, num_districts, initial_infected, steps, output_dir):
    """
    Run the SIERD simulation.

    Args:
        width: Width of the grid.
        height: Height of the grid.
        density: Density of the agents.
        transmission_rate: Probability of transmission per contact.
        latency_period: Number of steps an agent stays in the exposed state.
        infection_duration: Number of steps an agent stays in the infected state.
        recovery_rate: Probability of recovering from the infected state.
        policy: Policy applied to agents (e.g., Mask Policy Only, Lockdown Only)
        num_districts: Number of districts in the environment.
        initial_infected: Number of initially infected agents.
        steps: Number of steps to simulate.
    """

    model = SIERDModel(width, height, density, transmission_rate, latency_period, infection_duration, recovery_rate,
                       policy, num_districts, initial_infected)
    for _ in range(steps):
        model.step()
    results = model.datacollector.get_model_vars_dataframe()

    if policy == "Mayor":
        policy_filename = os.path.join(output_dir, f"policy_records_{policy.replace(' ', '_').lower()}.csv")
        model.export_policy_records(policy_filename)
        print(f"Policy records saved to {policy_filename}")

    return results

def save_results(results, filename):
    """
    Save the simulation results to a CSV file.

    Args:
        results: The results dataframe.
        filename: The filename to save the results.
    """
    results.to_csv(filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, default=10, help="Width of the grid")
    parser.add_argument("--height", type=int, default=10, help="Height of the grid")
    parser.add_argument("--density", type=float, default=8, help="Density of the agents")
    parser.add_argument("--transmission_rate", type=float, default=0.4, help="Transmission rate of the virus")
    parser.add_argument("--latency_period", type=int, default=15, help="Latency period of the virus")
    parser.add_argument("--infection_duration", type=int, default=50, help="Infection duration of the virus")
    parser.add_argument("--recovery_rate", type=float, default=0.3, help="Recovery rate from the virus")
    parser.add_argument("--num_districts", type=int, default=5, help="Number of districts in the environment")
    parser.add_argument("--initial_infected", type=int, default=50, help="Number of initially infected agents")
    parser.add_argument("--steps", type=int, default=500, help="Number of steps to simulate")
    parser.add_argument("--output_dir", type=str, default="results", help="Output directory to save the results")
    args = parser.parse_args()

    # Define policies
    policies = ["No Interventions", "Lockdown Only", "Mask Policy Only", "Combination of Lockdown and Mask Policy", "Mayor"]

    # Ensure the output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    for policy in policies:
        print(f"Running model with policy: {policy}")
        results = run_simulation(args.width, args.height, args.density, args.transmission_rate, args.latency_period,
                                 args.infection_duration, args.recovery_rate, policy, args.num_districts,
                                 args.initial_infected, args.steps, args.output_dir)

        csv_filename = os.path.join(args.output_dir, f"results_{policy.replace(' ', '_').lower()}.csv")
        save_results(results, csv_filename)
        print(f"Results saved to {csv_filename}")

        results.plot(title=f"Policy: {policy}")
        plt.show()
        