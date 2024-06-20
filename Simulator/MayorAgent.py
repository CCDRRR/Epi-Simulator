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
        self.policy_step_counter = {district_id: 0 for district_id in set(self.model.districts.values())}
        self.policy_duration = 42
        self.district_policies = {district_id: {"lockdown": False, "mask": False} for district_id in set(self.model.districts.values())}

    def step(self):
        # every step refresh
        if self.lockdown_active or self.mask_policy_active:
            self.policy_step_counter += 1

        for district_id in self.district_policies:
            infected_ratio = self.calculate_infected_ratio(district_id)
            mask_policy_threshold = 0.05
            lockdown_threshold = 0.1

            if self.policy_step_counter[district_id] >= self.policy_duration:
                if infected_ratio > lockdown_threshold and not self.district_policies[district_id]["lockdown"]:
                    self.enforce_lockdown(district_id, True)
                elif infected_ratio <= lockdown_threshold and self.district_policies[district_id]["lockdown"]:
                    self.enforce_lockdown(district_id, False)

                if infected_ratio > mask_policy_threshold and not self.district_policies[district_id]["mask"]:
                    self.enforce_mask_policy(district_id, True)
                elif infected_ratio <= mask_policy_threshold and self.district_policies[district_id]["mask"]:
                    self.enforce_mask_policy(district_id, False)

                self.policy_step_counter[district_id] = 0
            else:
                self.policy_step_counter[district_id] += 1

            print(
                f"Step {self.model.schedule.time}: District {district_id} policies: {self.district_policies[district_id]}")

        print(f"Policies at step {self.model.schedule.time}: {self.district_policies}")

    def calculate_infected_ratio(self, district_id):
        district_agents = [
            agent for agent in self.model.schedule.agents
            if isinstance(agent, SIERDAgent) and agent.district_id == district_id
        ]
        infected_agents = [agent for agent in district_agents if agent.state == "Infected"]
        return len(infected_agents) / len(district_agents) if district_agents else 0

    def enforce_lockdown(self, district_id, enforce):
        self.district_policies[district_id]["lockdown"] = enforce
        for agent in self.model.schedule.agents:
            if isinstance(agent, SIERDAgent) and agent.district_id == district_id:
                agent.isolated = enforce
        print(f"Lockdown {'enforced' if enforce else 'lifted'} in district {district_id}")

    def enforce_mask_policy(self, district_id, enforce):
        self.district_policies[district_id]["mask"] = enforce
        for agent in self.model.schedule.agents:
            if isinstance(agent, SIERDAgent) and agent.district_id == district_id:
                agent.wearing_mask = enforce
        print(f"Mask policy {'enforced' if enforce else 'lifted'} in district {district_id}")