#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 21:44:40 2024

@author: flora
"""

from mesa import Agent
from Agent import SIERDAgent

class MayorAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # proportion of infected persons in the total population
        infected_ratio = self.model.count_state(self.model, "Infected") / self.model.num_agents
        threshold = 0.2
        if self.model.policy == "Mayor":
            if infected_ratio > threshold:
                # lockdown if the infection rate exceeds the threshold
                for district_id in range(self.model.num_districts):
                    self.model.set_lockdown(district_id)
            else:
                # 如果感染比例低于阈值，解除封锁
                for district_id in range(self.model.num_districts):
                    self.model.lift_lockdown(district_id)
                    

        mask_policy_threshold = 0.05 

        if infected_ratio > mask_policy_threshold:
            self.enforce_mask_policy(True)
        else:
            self.enforce_mask_policy(False)

    def enforce_mask_policy(self, enforce):
        for agent in self.model.schedule.agents:
            if isinstance(agent, SIERDAgent):
                agent.wearing_mask = enforce