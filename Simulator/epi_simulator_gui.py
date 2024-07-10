# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:16:36 2024

@author: alext
"""

import argparse
import pandas as pd
import os
import matplotlib.pyplot as plt
from Environment import SIERDModel
from SALib.sample import saltelli
from mesa.batchrunner import BatchRunner
from SALib.analyze import sobol
import streamlit as st
from PIL import Image

def run_simulation(width, height, density, transmission_rate, latency_period, infection_duration, recovery_rate, policy, num_districts, initial_infected, steps):
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
    
    model = SIERDModel(width, height, density, transmission_rate, latency_period, infection_duration, recovery_rate, policy, num_districts, initial_infected)
    for _ in range(steps):
        model.step()
    results_cumulative = model.datacollector.get_model_vars_dataframe()
    return results_cumulative

def save_results(results, filename):
    """
    Save the simulation results to a CSV file.

    Args:
        results: The results dataframe.
        filename: The filename to save the results.
    """
    results.to_csv(filename)

def main():
    

    st.sidebar.title("Epi-Simulator")
    st.sidebar.write("Welcome to the Epi-Simulator for modeling the spread of infectious diseases and evaluating the effectiveness of various non-pharmaceutical interventions.")

    # Define the input parameters with descriptions
    width = st.sidebar.slider("Grid Width", min_value=10, max_value=50, value=10, step=1, help="The width of the simulation grid.")
    height = st.sidebar.slider("Grid Height", min_value=10, max_value=50, value=10, step=1, help="The height of the simulation grid.")
    density = st.sidebar.slider("Agent Density", min_value=0.1, max_value=10.0, value=8, step=0.1, help="The density of agents in the grid.")
    transmission_rate = st.sidebar.slider("Transmission Rate", min_value=0.1, max_value=1.0, value=0.4, step=0.1, help="The probability of transmission per contact.")
    latency_period = st.sidebar.slider("Latency Period", min_value=1, max_value=100, value=15, step=1, help="The number of steps an agent stays in the exposed state.")
    infection_duration = st.sidebar.slider("Infection Duration", min_value=1, max_value=100, value=50, step=1, help="The number of steps an agent stays in the infected state.")
    recovery_rate = st.sidebar.slider("Recovery Rate", min_value=0.1, max_value=1.0, value=0.3, step=0.1, help="The probability of recovering from the infected state.")
    num_districts = st.sidebar.slider("Number of Districts", min_value=1, max_value=10, value=5, step=1, help="The number of districts in the environment.")
    initial_infected = st.sidebar.slider("Initially Infected Agents", min_value=1, max_value=100, value=50, step=1, help="The number of agents initially infected.")
    steps = st.sidebar.slider("Simulation Steps", min_value=100, max_value=1000, value=500, step=100, help="The number of steps to simulate.")

    policy = st.sidebar.selectbox("Select Policy", options=["No Interventions", "Lockdown Only", "Mask Policy Only", "Combination of Lockdown and Mask Policy", "Mayor"], help="The policy to apply during the simulation.")
    
    st.title("Epi-Simulator")
    st.write("""
        ## SIERD Model
        The SIERD model is an epidemiological model that simulates the spread of infectious diseases through different stages:
        - **S**: Susceptible Population
        - **E**: Exposed Population
        - **I**: Infected Population
        - **R**: Recovered Population
        - **D**: Deceased Population
        - **β**: Transmission Rate
        - **σ**: Incubation Rate
        - **ϕe**: Asymptomatic Recovery Rate
        - **ϕr**: Symptomatic Recovery Rate
        - **ϕd**: Mortality Rate

        This model helps in understanding the impact of various non-pharmaceutical interventions (NPIs) like mask-wearing, lockdowns, and combined strategies on the spread of diseases.
    """)
    
    if st.sidebar.button("Run Simulation"):
        results_cumulative = run_simulation(width, height, density, transmission_rate, latency_period, infection_duration, recovery_rate, policy, num_districts, initial_infected, steps)
        
        # Display cumulative results
        st.subheader("Cumulative Simulation Results")
        st.line_chart(results_cumulative)

        # Display the results dataframe
        st.write("Dataframe of Simulation Results")
        st.dataframe(results_cumulative)

        # Save results
        csv_filename = f"results_{policy.replace(' ', '_').lower()}.csv"
        save_results(results_cumulative, csv_filename)
        
        # Provide a download link
        st.download_button(
            label="Download Results as CSV",
            data=results_cumulative.to_csv().encode('utf-8'),
            file_name=csv_filename,
            mime='text/csv',
        )
        st.success(f"Results saved to {csv_filename}")

    # Add copyright information
    st.sidebar.write("© 2024 Agent Based Modeling Course, Group 8, University of Amsterdam")

if __name__ == "__main__":
    main()

