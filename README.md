# Epi-Simulator
Epi-Simulator is a flexible and configurable agent-based simulation model designed to study the spread of epidemics under various intervention policies. The model implements the SIERD (Susceptible, Exposed, Infected, Recovered, Dead) framework and allows users to simulate different policies such as lockdowns and mask mandates to understand their impact on epidemic dynamics.

## Usage
### Command-Line Interface 
You can run the simulation and specify parameters via command-line arguments using **argparse**.
#### Example Command
```
python run_model.py --width 50 --height 50 --density 0.1 --transmission_rate 0.2 --latency_period 3 --infection_duration 14 --recovery_rate 0.95 --initial_infected 10 --policies "No Interventions,Lockdown Only,Mask Policy Only,Combination of Lockdown and Mask Policy" --steps 200 --output_dir ./results
```
### Parameters
* --width: Width of the grid (default: 50).
* --height: Height of the grid (default: 50).
* --density: Density of the agents in the grid (default: 0.1).
* --transmission_rate: Probability of transmission per contact (default: 0.2).
* --latency_period: Number of steps an agent stays in the exposed state (default: 3).
* --infection_duration: Number of steps an agent stays in the infected state (default: 14).
* --recovery_rate: Probability of recovering from the infected state (default: 0.95).
* --initial_infected: Initial number of infected agents (default: 10).
* --policies: Comma-separated list of policies to run (default: "No Interventions,Lockdown Only,Mask Policy Only,Combination of Lockdown and Mask Policy").
* --steps: Number of steps to run the model (default: 100).
* --output_dir: Directory to save the CSV files (default: ".").

### Output
* CSV Files: The simulation results for each policy are saved as CSV files in the specified output directory.
* Plots: The simulation results are plotted for each policy, providing a visual comparison of the impact of different interventions.
