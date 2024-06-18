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
        self.lockdown_active = False
        self.mask_policy_active = False
        self.policy_step_counter = 0
        self.policy_duration = 42  # duration

    def step(self):
        # every step refresh
        if self.lockdown_active or self.mask_policy_active:
            self.policy_step_counter += 1

        # proportion of infected persons in the total population
        infected_ratio = self.model.count_state(self.model, "Infected") / self.model.num_agents
        mask_policy_threshold = 0.05  # Mask policy threshold
        lockdown_threshold = 0.1  # Lockdown policy threshold

        # after 42 steps
        if self.policy_step_counter >= self.policy_duration:
            if infected_ratio > lockdown_threshold and not self.lockdown_active:
                self.enforce_lockdown(True)
            elif infected_ratio <= lockdown_threshold and self.lockdown_active:
                self.enforce_lockdown(False)

            if infected_ratio > mask_policy_threshold and not self.mask_policy_active:
                self.enforce_mask_policy(True)
            elif infected_ratio <= mask_policy_threshold and self.mask_policy_active:
                self.enforce_mask_policy(False)

            # reset counter
            self.policy_step_counter = 0

    def enforce_lockdown(self, enforce):
        self.lockdown_active = enforce
        for agent in self.model.schedule.agents:
            if isinstance(agent, SIERDAgent):
                agent.isolated = enforce

    def enforce_mask_policy(self, enforce):
        self.mask_policy_active = enforce
        for agent in self.model.schedule.agents:
            if isinstance(agent, SIERDAgent):
                agent.wearing_mask = enforce