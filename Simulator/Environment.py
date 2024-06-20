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
    def __init__(self, width, height, density, transmission_rate, latency_period, infection_duration, recovery_rate,
                 policy, num_districts, initial_infected):
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
        self.policy_history = []

        if policy == "Mayor":
            self.mayor = MayorAgent("Mayor", self)
        else:
            self.mayor = None

        for i in range(self.num_agents):
            district_id = random.choice(list(self.districts.values()))
            wearing_mask = False
            isolated = False
            if policy == "Mask Policy Only":
                wearing_mask = True
            elif policy == "Lockdown Only":
                isolated = True
            elif policy == "Combination of Lockdown and Mask Policy":
                wearing_mask = True
                isolated = True

            agent = SIERDAgent(i, self, district_id, wearing_mask, isolated)
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        infected_agents = self.random.sample(self.schedule.agents, k=initial_infected)
        for agent in infected_agents:
            agent.state = "Infected"
            agent.infection_time = self.schedule.time

        self.datacollector = DataCollector(
            model_reporters={"Susceptible": lambda m: self.count_state(m, "Susceptible"),
                             "Exposed": lambda m: self.count_state(m, "Exposed"),
                             "Infected": lambda m: self.count_state(m, "Infected"),
                             "Recovered": lambda m: self.count_state(m, "Recovered"),
                             "Dead": lambda m: self.count_state(m, "Dead")},
            agent_reporters={"state": "state", "district_id": lambda a: a.district_id}
        )

    def count_state(self, model, state):
        """
        Count the number of agents in a given state.

        Args:
            model: The model instance.
            state: The state to count.
        """
        return sum([1 for agent in model.schedule.agents if agent.state == state])

    def count_infected_by_district(self):
        district_counts = {district_id: 0 for district_id in set(self.districts.values())}
        for agent in self.schedule.agents:
            if agent.state == "Infected":
                district_id = self.districts.get(agent.pos, -1)
                if district_id != -1:
                    district_counts[district_id] += 1
        return district_counts

    def district_wise_infected(self, model):
        district_infected = {}
        for district_id in set(self.districts.values()):
            district_infected[district_id] = sum(
                1 for agent in model.schedule.agents if
                agent.state == "Infected" and self.districts[agent.pos] == district_id
            )
        return district_infected

    def create_districts(self, num_districts, width, height):
        districts = {}
        step = width // num_districts
        district_id = 0
        for i in range(num_districts):
            for j in range(num_districts):
                for x in range(i * step, (i + 1) * step):
                    for y in range(j * step, (j + 1) * step):
                        districts[(x, y)] = district_id
                district_id += 1
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

        if self.mayor:
            self.mayor.step()

        # Save the policy state
        if self.mayor:
            district_policies = {district_id: {"lockdown": policy["lockdown"], "mask": policy["mask"]}
                                 for district_id, policy in self.mayor.district_policies.items()}
        else:
            if self.policy == "Lockdown Only":
                district_policies = {district_id: {"lockdown": True, "mask": False} for district_id in
                                     set(self.districts.values())}
            elif self.policy == "Mask Policy Only":
                district_policies = {district_id: {"lockdown": False, "mask": True} for district_id in
                                     set(self.districts.values())}
            elif self.policy == "Combination of Lockdown and Mask Policy":
                district_policies = {district_id: {"lockdown": True, "mask": True} for district_id in
                                     set(self.districts.values())}
            else:
                district_policies = {district_id: {"lockdown": False, "mask": False} for district_id in
                                     set(self.districts.values())}

        self.policy_history.append({
            "step": self.schedule.time,
            "district_policies": district_policies
        })
        print(f"Policy history at step {self.schedule.time}: {self.policy_history[-1]}")
            
           