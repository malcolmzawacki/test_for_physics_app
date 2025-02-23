# utils/generators/collision_generator.py
import random
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

class CollisionGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="collision_")
    
    def generate_question(self, collision_type, difficulty):
        if collision_type == "Elastic Collision":
            return self._generate_elastic_collision(difficulty)
        else:
            return self._generate_inelastic_collision(difficulty)
        
    def numbers(self, difficulty):
        coin = random.randint(0,1)
        m1 = random.randint(1,difficulty)
        g = random.randint(2,difficulty)
        h = random.randint(1,difficulty)
        j = random.randint(1,difficulty)
        if coin == 1:
            g *= -1
            h *= -1
            j *= -1
        
        m2 = m1*g*h
        v2 = j*(1+g*h)
        v1 = v2*g
        v1_p = g*j*(2*h - g*h + 1)
        v2_p = j*(2*g + g*h - 1)
        impulse_2 = m2*(2*j*(g-1))
        impulse_1 = -1*impulse_2
        t_val = random.randint(-2,0)
        time = 10**t_val
        Force_1 = impulse_1//time
        Force_2 = -1*Force_1
        v3 = g*j*(h + 1)
        return m1, v1, m2, v2, v1_p, v2_p, v3, impulse_1, impulse_2, Force_1, Force_2, time
    
    def _generate_elastic_collision(self, difficulty):
        range = self.get_difficulty_range(difficulty)//2
        m1, v1, m2, v2, v1_p, v2_p, _, impulse_1, impulse_2, Force_1, Force_2, time = self.numbers(range)
        object1 = random_noun()
        object2 = random_noun()
        if v2 < 0:
            verb = "collides head on into"
        else:
            verb = "rear ends"
        if difficulty == "Easy":
            answer2 = 0
            unit2 = ""
            question = f"""A {m1:.2f} kg {object1} moving at {v1:.2f} m/s {verb} 
            a {m2:.2f} kg {object2} moving at {v2:.2f} m/s . 
            The {object1} is moving at {v1_p:.2f} after the collision. 
            How fast is the {object2} moving?"""
            answer = v2_p
            unit = f"{object2} final velocity (m/s)"
        elif difficulty == "Medium":
            answer2 = 0
            unit2 = ""
            question = f"""A {m1:.2f} kg {object1} moving at {v1:.2f} m/s {verb} 
            a {m2:.2f} kg {object2} moving at {v2:.2f} m/s. 
            They experience a force of {abs(Force_1):.2f} Newtons, and the collision lasts {time} seconds.
            How fast is {object1} moving after the collision?"""
            answer = v1_p
            unit = f"{object1} final velocity (m/s)"

        return question, answer, unit, answer2, unit2
    
    
    def _generate_inelastic_collision(self, difficulty):
        range = self.get_difficulty_range(difficulty)
        m1, v1, m2, v2, _, _, v3, impulse_1, impulse_2, Force_1, Force_2, time = self.numbers(range)
        object1 = random_noun()
        object2 = random_noun()
        if v2 < 0:
            verb = "collides head on into"
        else:
            verb = "rear ends"
        if difficulty == "Easy":
            answer2 = 0
            unit2 = ""
            question = f"""A {m1:.2f} kg {object1} moving at {v1:.2f} m/s {verb} 
            a {m2:.2f} kg {object2} moving at {v2:.2f} m/s . They smush together. 
            How fast are they moving together?"""
            answer = v3
            unit = f"{object1} and {object2} combined final velocity (m/s)"
        elif difficulty == "Medium":
            answer2 = 0
            unit2 = ""
            question = f"""A {m1:.2f} kg {object1} moving at {v1:.2f} m/s {verb} 
            a {m2:.2f} kg {object2}. They smush together and move with a combined velocity of {v3:.2f} m/s. 
            How fast was {object2} moving before the collision?"""
            unit = f"{object2} initial velocity (m/s)"
            answer = v2


        return question, answer, unit, answer2, unit2