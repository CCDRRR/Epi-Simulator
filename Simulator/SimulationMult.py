import argparse
import pandas as pd
import os
import matplotlib.pyplot as plt
from run_model import run_simulation


def simulate_multiple_runs(params, policies, num_simulations):
    all_results = {}
    summary_stats = []

    for policy in policies:
        policy_results = [run_simulation(**params, policy=policy) for _ in range(num_simulations)]

        combined_results = pd.concat(policy_results, axis=1)
        mean_results = combined_results.groupby(combined_results.columns, axis=1).mean()
        std_results = combined_results.groupby(combined_results.columns, axis=1).std()

        all_results[policy] = (mean_results, std_results)

        # Record peak infected and total dead
        peak_infected = mean_results['Infected'].max()
        total_dead = mean_results['Dead'].iloc[-1]
        summary_stats.append({
            'Policy': policy,
            'Density': params['density'],
            'Transmission Rate': params['transmission_rate'],
            'Latency Period': params['latency_period'],
            'Infection Duration': params['infection_duration'],
            'Recovery Rate': params['recovery_rate'],
            'Peak Infected': peak_infected,
            'Total Dead': total_dead
        })

    return all_results, summary_stats


def plot_results(all_results, params, policies, output_dir):
    for policy, (mean_results, std_results) in all_results.items():
        plt.figure(figsize=(12, 8))  # Adjust figure size

        for column in mean_results.columns:
            plt.plot(mean_results[column], label=column)
            plt.fill_between(mean_results.index,
                             mean_results[column] - 1.96 * std_results[column],
                             mean_results[column] + 1.96 * std_results[column], alpha=0.3)

        title_text = (f'Policy: {policy}\nDensity: {params["density"]}, Transmission Rate: {params["transmission_rate"]}, '
                      f'Latency Period: {params["latency_period"]}, Infection Duration: {params["infection_duration"]}, '
                      f'Recovery Rate: {params["recovery_rate"]}')
        plt.title(title_text, fontsize=10)  # Adjust title font size
        plt.legend()
        plt.xlabel('Time Steps')
        plt.ylabel('Number of Individuals')

        # Create a unique filename for each combination of parameters and policy
        filename = (f'results_{policy.replace(" ", "_").lower()}_density{params["density"]}_'
                    f'transmission{params["transmission_rate"]}_latency{params["latency_period"]}_'
                    f'infection{params["infection_duration"]}_recovery{params["recovery_rate"]}.png')
        plt.savefig(os.path.join(output_dir, filename))
        plt.close()


if __name__ == "__main__":
    output_dir = 'results'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_params = {
        'width': 10,
        'height': 10,
        'density': 10,
        'transmission_rate': 0.6,
        'latency_period': 56,
        'infection_duration': 28,
        'recovery_rate': 0.1,
        'num_districts': 3,
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

    # Parameters to vary
    recovery_rates = [0.1, 0.5, 0.7]
    infection_durations = [28, 56, 112]

    all_summary_stats = []

    for recovery_rate in recovery_rates:
        for infection_duration in infection_durations:
            params = base_params.copy()
            params['recovery_rate'] = recovery_rate
            params['infection_duration'] = infection_duration

            all_results, summary_stats = simulate_multiple_runs(params, policies, num_simulations)
            plot_results(all_results, params, policies, output_dir)

            all_summary_stats.extend(summary_stats)

    summary_df = pd.DataFrame(all_summary_stats)
    summary_df.to_csv(os.path.join(output_dir, 'summary_stats.csv'), index=False)
    print("Simulation completed and summary statistics saved.")
