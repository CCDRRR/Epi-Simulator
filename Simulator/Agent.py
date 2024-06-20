# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 17:32:03 2024

@author: alext
"""

import numpy as np
import random
from mesa import Agent


class SIERDAgent(Agent):
    def __init__(self, unique_id, model, district_id, wearing_mask=False, isolated=False, recovered=False):
        """
        Initialize a SIERDAgent.

        Args:
            unique_id: The unique ID of the agent.
            model: The model instance.
            wearing_mask: A boolean indicating if the agent is wearing a mask (default: False).
            isolated: A boolean indicating if the agent is isolated (default: False).
            recovered: A boolean indicating if the agent has recovered (default: False).
        """
        super().__init__(unique_id, model)
        super().__init__(unique_id, model)
        self.state = "Susceptible"
        self.infection_time = 0
        self.wearing_mask = wearing_mask
        self.isolated = isolated
        self.recovered = recovered
        self.infection_history = []
        self.district_id = district_id  # Assign district ID to agent
        self.residence_area = (random.randint(0, model.grid.width - 1), random.randint(0, model.grid.height - 1))
        self.workplace = (random.randint(0, model.grid.width - 1), random.randint(0, model.grid.height - 1))

        # Initialize residence and workplace
        self.residence_area = (random.randint(0, model.grid.width - 1), random.randint(0, model.grid.height - 1))
        self.workplace = (random.randint(0, model.grid.width - 1), random.randint(0, model.grid.height - 1))

    def step(self):
        """
        The step method defines the agent's behavior at each time step.
        """
        if self.isolated:
            if self.decide_to_move_during_lockdown():
                self.move_randomly()
        else:
            if self.model.time_of_day == "morning":
                self.move_to_work()
            elif self.model.time_of_day == "afternoon":
                self.move_randomly()
            elif self.model.time_of_day == "night":
                self.move_to_residence()

        if self.state == "Susceptible":
            self.check_exposure()  # Check if the agent gets exposed to the virus
        elif self.state == "Exposed":
            self.progress_to_infected()  # Progress from exposed to infected state
        elif self.state == "Infected":
            self.infect_others()  # Try to infect other susceptible agents
            self.progress_to_recovered_or_dead()  # Recover or die after the infection duration
        elif self.state == "Recovered":
            self.check_reinfection()  # Check if the recovered agent gets re-exposed to the virus
        elif self.state == "Dead":
            pass  # No action for dead agents

    def decide_to_wear_mask(self):
        """
        Use a Logit model to decide whether the agent should wear a mask.
        """
        # Define the features for the Logit model
        features = np.array([
            1,  # Bias term
            1 if self.state in ["Infected", "Exposed"] else 0,  # Health state
            self.model.transmission_rate,  # Environmental factor (transmission rate from model)
            1 if self.infection_history else 0  # Infection history
        ])

        # Define the Logit model parameters (these should be determined based on data or assumptions)
        beta = np.array([0.5, 1.0, 2.0, 1.5])  # Example parameters, requires paper or research to adjust

        # Introduce a random error term to simulate unobserved factors
        epsilon = np.random.normal(0, 1)  # Standard normal distribution

        # Calculate the logit value with the error term
        logit = np.dot(features, beta) + epsilon
        probability = 1 / (1 + np.exp(-logit))

        # Decide whether to wear a mask
        self.wearing_mask = probability > 0.5

    def move_to_work(self):
        """
        Move the agent to its workplace.
        """
        if not self.isolated and not self.model.is_lockdown(self.workplace):
            self.model.grid.move_agent(self, self.workplace)

    def move_to_residence(self):
        """
        Move the agent to its residence area.
        """
        if not self.isolated and not self.model.is_lockdown(self.residence_area):
            self.model.grid.move_agent(self, self.residence_area)

    # def move_randomly(self):
    #    """
    #    Move the agent to a random neighboring cell.
    #    """
    #    if not self.isolated:
    #        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
    #        new_position = random.choice(possible_steps)
    #        if not self.model.is_lockdown(new_position):
    #            self.model.grid.move_agent(self, new_position)

    def check_exposure(self):
        """
        Check if the susceptible agent gets exposed to the virus from infected neighbors.
        """
        if self.isolated:
            return  # If isolated, the agent does not get exposed
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if agent.state == "Infected":
                transmission_rate = self.model.transmission_rate
                if self.wearing_mask:
                    transmission_rate *= 0.2  # Reduce transmission rate if wearing a mask
                if random.random() < transmission_rate:
                    self.state = "Exposed"  # Change state to exposed
                    self.infection_time = self.model.schedule.time  # Record the time of exposure
                    break

    def progress_to_infected(self):
        """
        Progress from the exposed state to the infected state after the latency period.
        """
        if self.model.schedule.time - self.infection_time >= self.model.latency_period:
            self.state = "Infected"  # Change state to infected

    def infect_others(self):
        """
        Infect susceptible neighbors if the agent is in the infected state.
        """
        if self.isolated:
            return  # If isolated, the agent does not infect others
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if agent.state == "Susceptible":
                transmission_rate = self.model.transmission_rate
                if self.wearing_mask:
                    transmission_rate *= 0.2  # Reduce transmission rate if wearing a mask
                if agent.recovered:
                    transmission_rate *= 0.5  # Lower transmission rate for recovered individuals
                if random.random() < transmission_rate:
                    agent.state = "Exposed"  # Change neighbor's state to exposed
                    agent.infection_time = self.model.schedule.time  # Record the time of exposure

    def progress_to_recovered_or_dead(self):
        """
        Progress from the infected state to either recovered or dead after the infection duration.
        """
        if self.model.schedule.time - self.infection_time >= self.model.infection_duration:
            if random.random() < self.model.recovery_rate:
                self.state = "Recovered"  # Change state to recovered
                self.recovered = True  # Mark the agent as recovered
                self.infection_history.append(self.model.schedule.time)  # Add recovery time to infection history
                self.decide_to_wear_mask()  # Decide to wear a mask based on new infection history
            else:
                self.state = "Dead"  # Change state to dead

    def check_reinfection(self):
        """
        Check if the recovered agent gets re-exposed to the virus.
        """
        if self.isolated:
            return  # If isolated, the agent does not get re-exposed
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if agent.state == "Infected":
                transmission_rate = self.model.transmission_rate  # Same reinfection rate as initial infection
                if self.wearing_mask:
                    transmission_rate *= 0.2  # Reduce transmission rate if wearing a mask
                if random.random() < transmission_rate:
                    self.state = "Exposed"  # Change state to exposed again
                    self.infection_time = self.model.schedule.time  # Record the time of re-exposure
                    break

    def decide_to_move_during_lockdown(self):
        """
        Decide whether the agent moves during lockdown using a normal distribution.
        """
        # 使用正态分布决定是否移动
        move_probability = np.random.normal(0.2, 0.05)
        return move_probability > 0.15

    def move_randomly(self):
        """
        Move the agent to a random neighboring cell.
        """
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)