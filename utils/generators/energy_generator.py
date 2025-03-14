from random import randint as ri
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
try:
    from .base_generator import BaseGenerator
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from utils.generators.base_generator import BaseGenerator

from utils.word_lists import random_noun

class EnergyGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="energy_")

    def get_difficulty_range(self, difficulty):
        if difficulty == "Easy":
            return 5
        elif difficulty == "Hard":
            return 20
        return 10

    def kinetic_energy(self,difficulty):
        upper = self.get_difficulty_range(difficulty)
        mass = ri(1,upper)
        velocity = ri(1,upper)
        flip = ri(0,1)
        if flip == 0:
            mass*=2
        else:
            velocity*=2
        return mass, velocity, 0.5*mass*velocity**2

    def gravitational_potential_energy(self,difficulty):
        upper = self.get_difficulty_range(difficulty)
        mass = ri(1,upper)
        height = ri(1,upper)
        return mass, height, mass*10*height

    def elastic_potential_energy(self,difficulty):
        upper = self.get_difficulty_range(difficulty)
        spring_constant = ri(1,upper)
        compression = ri(1,upper)
        flip = ri(0,1)
        if flip == 0:
            spring_constant*=2
        else:
            compression*=2
        return spring_constant, compression, 0.5*spring_constant*compression**2

    def work(self,difficulty):
        upper = self.get_difficulty_range(difficulty)
        force = ri(1,upper)
        distance = ri(1,upper)
        return force, distance, force*distance

    def elastic_problem(self,difficulty):
        spring_constant, compression, elastic_e = self.elastic_potential_energy(difficulty)
        q_type = ri(0,2)
        dirn = ri(0,1)
        dirn_string = "compressed" if dirn == 0 else "stretched"
        {}
        if q_type == 0:
            question = f"""A spring with strength {spring_constant} N/m is {dirn_string} by {compression} meters.
            What is the amount of elastic potential energy held in the spring?"""
            answer = elastic_e
            unit = "Joules"
        elif q_type == 1:
            question = f"""A spring with strength {spring_constant} N/m contains {elastic_e} Joules of elastic potential energy.
            How much was this spring {dirn_string}?"""
            answer = compression
            unit = "meters"
        else:
            question = f"""A spring is {dirn_string} by {compression} meters, and contains {elastic_e} Joules of elastic potential energy.
            What is the strength of the spring constant?"""
            answer = spring_constant
            unit = "N/m"

        return question, answer, unit
    
    def kinetic_problem(self,difficulty):
        mass, velocity, kinetic_e = self.kinetic_energy(difficulty)
        q_type = ri(0,2)
        noun = random_noun()
        if q_type == 0:
            question = f"""How much kinetic energy does a {mass} kg {noun} moving at {velocity} m/s have?"""
            answer = kinetic_e
            unit = "Joules"
        elif q_type == 1:
            question = f"""How fast would a {mass} kg {noun} have to move to have {kinetic_e} Joules of kinetic energy?"""
            answer = velocity
            unit = "m/s"
        else:
            question = f"""How much mass would a {noun} moving at {velocity} m/s need to have to contain {kinetic_e} Joules of kinetic energy?"""
            answer = mass
            unit = "kg"

        return question, answer, unit
    
    def gravitational_problem(self,difficulty):
        mass, height, gravit_e = self.gravitational_potential_energy(difficulty)
        q_type = ri(0,2)
        noun = random_noun()
        if q_type == 0:
            question = f"""How much gravitational potential energy does a {mass} kg {noun} 
            held {height} meters above the ground have?"""
            answer = gravit_e
            unit = "Joules"
        elif q_type == 1:
            question = f"""How high up would a {mass} kg {noun} have to be to have 
            {gravit_e} Joules of gravitational potential energy?"""
            answer = height
            unit = "meters"
        else:
            question = f"""How much mass would a {noun} at a height of {height} meters need to have 
            to contain {gravit_e} Joules of gravitational potential energy?"""
            answer = mass
            unit = "kg"

        return question, answer, unit
    
    def work_problem(self,difficulty):
        force, distance, work = self.work(difficulty)
        q_type = ri(0,2)
        noun = random_noun()
        if q_type == 0:
            question = f"""A {noun} is moved {distance} meters by a {force} Newton force. How much work was done?"""
            answer = work
            unit = "Joules"
        elif q_type == 1:
            question = f"""Over how much distance would a {force} Newton force have to push a {noun} before it did {work} Joules of work?"""
            answer = distance
            unit = "meters"
        else:
            question = f"""{work} Joules of work are done on a {noun} over a distance of {distance} meters.
            How much force was applied?"""
            answer = force
            unit = "Newtons"

        return question, answer, unit

    
    def kinetic_gravitational_problem(self,difficulty):
        mass, velocity, _ = self.kinetic_energy(difficulty)
        height = velocity**2 / 20
        q_type = ri(0,1)
        noun = random_noun()
        if q_type == 0:
            question = f"""A {mass} kg {noun} is dropped from a height of {height:.2f} meters.
            How fast is it moving when it hits the ground?"""
            answer = velocity
            unit = "m/s"
        else:
            question = f"""A {mass} kg {noun} is released from rest and hits the ground at {velocity} m/s.
            How high up was it dropped from?"""
            answer = height
            unit = "meters"

        return question, answer, unit
    
    def elastic_gravitational_problem(self, difficulty):
        spring_constant, compression, elastic_e = self.elastic_potential_energy(difficulty)
        upper = self.get_difficulty_range(difficulty)
        mass = ri(1,upper)
        height = elastic_e / 20*mass

        q_type = ri(0,3)
        noun = random_noun()
        if q_type == 0:
            # find k
            question = f"""A {mass} kg {noun} is dropped from a height of {height:.2f} meters.
            A spring has to compress by {compression} meters to stop it. How strong is the spring?"""
            answer = spring_constant
            unit = "N/m"
        elif q_type == 1:
            # find height
            question = f"""A {mass} kg {noun} is released from rest and dropped on a spring of strength {spring_constant} N/m.
            If the spring compresses {compression} meters before the {noun} comes to rest, how high up was it dropped from?"""
            answer = height
            unit = "meters"
        elif q_type == 2:
            # find compression
            question = f"""A {mass} kg {noun} is dropped from {height} meters onto a spring of strength {spring_constant} N/m.
            How much does the spring have to compress to bring the {noun} to rest?"""
            answer = compression
            unit = "meters"
        else:
            question = f"""A {noun} is dropped from {height} meters onto a spring of strength {spring_constant} N/m.
            If the spring compresses by {compression} meters to bring the {noun} to rest, how much mass does the {noun} have?"""
            answer = mass
            unit = "kilograms"

        return question, answer, unit


    def elastic_kinetic_problem(self, difficulty):
            spring_constant, compression, _ = self.elastic_potential_energy(difficulty)
            upper = self.get_difficulty_range(difficulty)
            mass = ri(1,upper)
            velocity = compression  * (spring_constant / mass )**(1/2)
            
            q_type = ri(0,3)
            noun = random_noun()
            if q_type == 0:
                # find k
                question = f"""A {mass} kg {noun} strikes a spring while moving as {velocity:.2f} m/s. 
                The spring has to compress by {compression} meters to stop it. How strong is the spring?"""
                answer = spring_constant
                unit = "N/m"
            elif q_type == 1:
                # find velocity
                question = f"""A {mass} kg {noun} hits a spring of strength {spring_constant} N/m.
                If the spring compresses {compression} meters before the {noun} comes to rest, how fast was the {noun} initially moving?"""
                answer = velocity
                unit = "m/s"
            elif q_type == 2:
                # find compression
                question = f"""A {mass} kg {noun} moving at {velocity:.2f} m/s hits a spring of strength {spring_constant} N/m.
                How much does the spring have to compress to bring the {noun} to rest?"""
                answer = compression
                unit = "meters"
            else:
                question = f"""A {noun} moving as {velocity:.2f} m/s hits a spring of strength {spring_constant} N/m.
                If the spring compresses by {compression} meters to bring the {noun} to rest, how much mass does the {noun} have?"""
                answer = mass
                unit = "kilograms"

            return question, answer, unit