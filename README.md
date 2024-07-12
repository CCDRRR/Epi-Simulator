# Epi-Simulator
Epi-Simulator is a flexible and configurable agent-based simulation model designed to study the spread of epidemics under various intervention policies. The model implements the SIERD (Susceptible, Exposed, Infected, Recovered, Dead) framework and allows users to simulate different policies such as lockdowns and mask mandates to understand their impact on epidemic dynamics.

## File Structure

### Agent.py
This file defines the agent class used in the simulation. Each agent represents an individual in the SEIRD model and contains properties and methods related to their state and behavior.

### AgentMayor.py
This file extends the basic agent class to include additional behaviors and properties specific to agents that are governed by the Mayor Policy.

### Environment.py
This file defines the environment in which the agents interact. It sets up the grid, manages agent interactions, and updates the state of the simulation at each step.

### run_model.py
This is the main script for running the simulation. It sets up the environment and agents, configures the simulation parameters via command-line arguments, and runs the simulation.

### epi_simulator_gui.py
This file provides the source code for the browser-based graphical user interface (GUI). It allows users to configure and run simulations through a web interface.

### gui.py
This file provides the desktop graphical user interface (GUI) for running the simulation. It allows users to input parameters through a visual interface rather than using command-line arguments.

### SA.ipynb
This Jupyter Notebook performs post-simulation analysis, including the Sobol Sensitivity Analysis, to evaluate the impact of different parameters on the simulation outcomes.

### SA-Mayor.ipynb
This Jupyter Notebook extends the sensitivity analysis to include scenarios governed by the Mayor Policy.

### requirements.txt
This file lists all the Python dependencies required to run the project. Install them using:

```bash
pip install -r requirements.txt
```
## How to Run the Simulation
### Command-Line Interface 
You can run the simulation and specify parameters via command-line arguments using **argparse**.
#### Example Command
```
python run_model.py --width 10 --height 10 --density 8 --transmission_rate 0.4 --latency_period 15 --infection_duration 50 --recovery_rate 0.3 --num_districts -- 5 initial_infected 50 --policies: Comma-separated list of policies to run "No Interventions,Lockdown Only,Mask Policy Only,Combination of Lockdown and Mask Policy" --steps 500 --output_dir "results"
```
### Parameters
* --width: Width of the grid (default: 10).
* --height: Height of the grid (default: 10).
* --density: Density of the agents in the grid (default: 8).
* --transmission_rate: Probability of transmission per contact (default: 0.4).
* --latency_period: Number of steps an agent stays in the exposed state (default: 15).
* --infection_duration: Number of steps an agent stays in the infected state (default: 50).
* --recovery_rate: Probability of recovering from the infected state (default: 0.3).
* --num_districts: Number of districts in the environment (default: 5).
* --initial_infected: Initial number of infected agents (default: 50).
* --policies: Comma-separated list of policies to run (default: "No Interventions,Lockdown Only,Mask Policy Only,Combination of Lockdown and Mask Policy").
* --steps: Number of steps to run the model (default: 500).
* --output_dir: Directory to save the CSV files (default: "results").

### Desktop Interface
You can also run the simulation using a desktop graphical user interface (GUI). The GUI is located in the GUI file. To start the GUI, run:
```
python GUI.py
```
### Online Interface
For convenience, an online interface is available at the following URL:
```
https://ccdrrr-epi-simulator-simulatorepi-simulator-gui-simulato-lhvfqd.streamlit.app/
```
Use the online interface to run simulations and visualize results directly in your web browser.

### Output
* CSV Files: The simulation results for each policy are saved as CSV files in the specified output directory.
* Plots: The simulation results are plotted for each policy, providing a visual comparison of the impact of different interventions.

## License
MIT License

Copyright (c) 2024 University of Amsterdam

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

