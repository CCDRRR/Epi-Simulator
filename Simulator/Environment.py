# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 17:33:57 2024

@author: alext
"""

import random
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from Agent import SIERDAgent
import numpy as np
from AgentMayor import AgentMayor

class SIERDModel(Model):
    def __init__(self, width, height, density, transmission_rate, latency_period, infection_duration, recovery_rate, policy, num_districts, initial_infected,mask_policy=False, lockdown=False):
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
            num_districts: Number of districts in the environment.
            initial_infected: Number of initially infected agents.
            mask_policy: Initial mask policy status (default: False).
            lockdown: Initial lockdown status (default: False).
        """
        self.num_agents = int(width * height * density)
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.transmission_rate = transmission_rate
        self.latency_period = latency_period
        self.infection_duration = infection_duration
        self.recovery_rate = recovery_rate
        self.policy = policy
        self.time_of_day = "morning"
        self.num_districts = num_districts
        self.mask_policy = mask_policy
        self.lockdown = lockdown
        self.mayor = None
        
        # Initialize agents
        for i in range(self.num_agents):
            wearing_mask = False
            isolated = False
            if policy == "Mask Policy Only":
                self.mask_policy = True
            elif policy == "Lockdown Only":
                self.lockdown = True
            elif policy == "Combination of Lockdown and Mask Policy":
                self.mask_policy = True
                self.lockdown = True
            
            # Create and place agent in a random position on the grid
            agent = SIERDAgent(i, self, wearing_mask, isolated)
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        # Initialize some agents as infected
        infected_agents = self.random.sample(self.schedule.agents, k=initial_infected)
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
        return sum([1 for agent in model.schedule.agents if isinstance(agent, SIERDAgent) and agent.state == state])

    def create_districts(self, num_districts, width, height):
        districts = {}
        step = width // num_districts
        for i in range(num_districts):
            for j in range(num_districts):
                district_id = i * num_districts + j
                for x in range(i * step, (i + 1) * step):
                    for y in range(j * step, (j + 1) * step):
                        districts[(x, y)] = district_id
        return districts
    
    # def adjust_parameters(self):
        time = self.schedule.time
        self.transmission_rate *= np.exp(-0.01 * time) # Transmission rate decreases over time
        
       # for agent in self.schedule.agents:
       #     agent.latency_period = max(1, agent.latency_period - 0.01 * time) # Latency period decrease over time
       #     agent.infection_duration = max(1, agent.infection_duration - 0.01 * time) # Infection duration decrease over time
       #     agent.recovery_rate = max(1, agent.recovery_rate + 0.03 * time ) # Recovery rate increases over time
            

    def step(self):
        #self.adjust_parameters()
        self.datacollector.collect(self)
        self.schedule.step()
        
        # Update time of day
        if self.time_of_day == "morning":
            self.time_of_day = "afternoon"
        elif self.time_of_day == "afternoon":
            self.time_of_day = "evening"
        elif self.time_of_day =="evening":
            self.time_of_day = "night"
        else:
            self.time_of_day = "morning"
        # If Mayor policy is active, execute Mayor's step
        if self.mayor:
            self.mayor.step()
    
    def export_policy_records(self, filename):
        """
        Export the policy records if the Mayor policy is active.
        
        Args:
            filename: The filename to export the records.

        """
        if self.mayor:
            self.mayor.export_policy_records(filename)