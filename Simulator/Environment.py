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
from MayorAgent import MayorAgent

class SIERDModel(Model):
    def __init__(self, width, height, density, transmission_rate, latency_period, infection_duration, recovery_rate, policy, num_districts, initial_infected):
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
            initial_infected: Number of initially infected agents
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
        self.districts = self.create_districts(num_districts, width, height)
        self.lockdown_areas = set()
        self.mayor = MayorAgent("Mayor", self)


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
            elif policy == "Mayor":
                wearing_mask = False
                isolated = False  
                
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
        return sum([1 for agent in model.schedule.agents if agent.state == state])

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

    def is_lockdown(self, area):
        return self.districts.get(area) in self.lockdown_areas

    def set_lockdown(self, district_id):
        self.lockdown_areas.add(district_id)

    def lift_lockdown(self, district_id):
        self.lockdown_areas.discard(district_id)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        if self.time_of_day == "morning":
            self.time_of_day = "afternoon"
        elif self.time_of_day == "afternoon":
            self.time_of_day = "night"
        else:
            self.time_of_day = "morning"
            
           