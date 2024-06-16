# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 17:33:57 2024

@author: alext
"""

import random
import pandas as pd
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from Agent import SIERDAgent

class SIERDModel(Model):
    def __init__(self, width, height, density, transmission_rate, latency_period, infection_duration, recovery_rate, policy, initial_infected):
        """
        Initialize a SIERDModel.

        Args:
            width: Width of the grid.
            height: Height of the grid.
            density: Density of the agents in the grid.
            transmission_rate: Probability of transmission per contact.
            latency_period: Number of steps an agent stays in the exposed state.
            infection_duration: Number of steps an agent stays in the infected state.
            recovery_rate: Probability of recovering from the infected state.
            policy: Policy applied to agents (e.g., Mask Policy Only, Lockdown Only)
            initial_infected: Initial number of infected agents.
        """
        self.num_agents = int(width * height * density)
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.transmission_rate = transmission_rate
        self.latency_period = latency_period
        self.infection_duration = infection_duration
        self.recovery_rate = recovery_rate
        self.policy = policy
        self.initial_infected = initial_infected

        for i in range(self.num_agents):
            wearing_mask = False
            isolated = False
            if policy == "Mask Policy Only":
                wearing_mask = True
            elif policy == "Lockdown Only":
                isolated = True
            elif policy == "Combination of Lockdown and Mask Policy":
                wearing_mask = True
                isolated = True
            
            agent = SIERDAgent(i, self, wearing_mask, isolated)
            self.schedule.add(agent)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        # Initialize some agents as infected
        infected_agents = random.sample(self.schedule.agents, k=self.initial_infected)
        for agent in infected_agents:
            agent.state = "Infected"
            agent.infection_time = self.schedule.time

        self.datacollector = DataCollector(
            {"Susceptible": lambda m: self.count_state(m, "Susceptible"),
             "Exposed": lambda m: self.count_state(m, "Exposed"),
             "Infected": lambda m: self.count_state(m, "Infected"),
             "Recovered": lambda m: self.count_state(m, "Recovered"),
             "Dead": lambda m: self.count_state(m, "Dead")})

    def count_state(self, model, state):
        """
        Count the number of agents in a given state.

        Args:
            model: The model instance.
            state: The state to count.
        """
        return sum([1 for agent in model.schedule.agents if agent.state == state])

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def get_results_dataframe(self):
        """
        Get the results as a pandas DataFrame.
        """
        return self.datacollector.get_model_vars_dataframe()

    def save_results_to_csv(self, filename):
        """
        Save the results to a CSV file.

        Args:
            filename: The name of the CSV file.
        """
        df = self.get_results_dataframe()
        df.to_csv(filename, index_label="Step")