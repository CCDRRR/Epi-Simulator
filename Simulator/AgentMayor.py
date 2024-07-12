# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 00:42:50 2024

@author: alext
"""

from mesa import Agent
import pandas as pd
from Agent import SIERDAgent

class AgentMayor(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.policy_duration = 28  # 7 days * 4 time steps per day
        self.lockdown_policies = {}  # Track lockdown durations per district
        self.mask_policies = {}  # Track mask policy durations per district

    def step(self):
        district_infection_rates = self.calculate_infection_rates()
        for district_id, infection_rate in district_infection_rates.items():
            if infection_rate > 0.3:
                if district_id not in self.lockdown_policies:
                    self.model.set_lockdown(district_id)
                    self.lockdown_policies[district_id] = self.policy_duration
                    self.record_policy("initiate", district_id, "lockdown")
                else:
                    self.record_policy("implemented", district_id, "lockdown")
                
                if district_id not in self.mask_policies:
                    self.model.mask_policy[district_id] = True
                    self.mask_policies[district_id] = self.policy_duration
                    self.record_policy("initiate", district_id, "mask")
                else:
                    self.record_policy("implemented", district_id, "mask")
            else:
                if district_id in self.lockdown_policies:
                    self.lockdown_policies[district_id] -= 1
                    if self.lockdown_policies[district_id] <= 0:
                        self.model.lift_lockdown(district_id)
                        del self.lockdown_policies[district_id]
                        self.record_policy("lifted", district_id, "lockdown")
                
                if district_id in self.mask_policies:
                    self.mask_policies[district_id] -= 1
                    if self.mask_policies[district_id] <= 0:
                        self.model.mask_policy[district_id] = False
                        del self.mask_policies[district_id]
                        self.record_policy("lifted", district_id, "mask")

    def calculate_infection_rates(self):
        infection_rates = {district_id: 0 for district_id in range(self.model.num_districts)}
        for agent in self.model.schedule.agents:
            if isinstance(agent, SIERDAgent):
                district_id = self.model.districts[agent.pos]
                if agent.state == "Infected":
                    infection_rates[district_id] += 1
        for district_id in infection_rates:
            district_population = sum(1 for agent in self.model.schedule.agents if isinstance(agent, SIERDAgent) and self.model.districts[agent.pos] == district_id)
            if district_population > 0:
                infection_rates[district_id] /= district_population
        return infection_rates

    def record_policy(self, status, district_id, policy_type):
        with open("policy_log.csv", "a") as f:
            f.write(f"{self.model.schedule.time},{status},{district_id},{policy_type}\n")