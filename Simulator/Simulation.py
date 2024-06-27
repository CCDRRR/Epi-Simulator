import argparse
import pandas as pd
import os
import matplotlib.pyplot as plt
from run_model import run_simulation

def simulate_multiple_runs(params, policies, num_simulations):
    all_results = {}
    
    for policy in policies:
        policy_results = [run_simulation(**params, policy=policy) for _ in range(num_simulations)]
        
        combined_results = pd.concat(policy_results, axis=1)
        mean_results = combined_results.groupby(combined_results.columns, axis=1).mean()
        std_results = combined_results.groupby(combined_results.columns, axis=1).std()
        
        all_results[policy] = (mean_results, std_results)
    
    return all_results

if __name__ == "__main__":
    params = {
        'width': 10,
        'height': 10,
        'density': 8,
        'transmission_rate': 0.4,
        'latency_period': 15,
        'infection_duration': 50,
        'recovery_rate': 0.3,
        'num_districts': 5,
        'initial_infected': 50,
        'steps': 500
    }
    policies = [
        'No Interventions',
        'Mask Policy Only',
        'Lockdown Only',
        'Combination of Lockdown and Mask Policy',
        'Mayor'
    ]
    num_simulations = 20

    all_results = simulate_multiple_runs(params, policies, num_simulations)

    # plot
    for policy, (mean_results, std_results) in all_results.items():
        plt.figure()
        
        for column in mean_results.columns:
            plt.plot(mean_results[column])
            plt.fill_between(mean_results.index,
                             mean_results[column] - 1.96 * std_results[column],
                             mean_results[column] + 1.96 * std_results[column], alpha=0.3)
        
        plt.title(f'{policy}')
        plt.legend(mean_results.columns)
        plt.show()
