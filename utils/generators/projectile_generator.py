# utils/generators/projectile_generator.py
import math
import random
import sys
from pathlib import Path

try:
    from .base_generator import BaseGenerator
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from utils.generators.base_generator import BaseGenerator

#from base_generator import BaseGenerator
from utils.word_lists import random_noun, random_proj_verb # does not need 


class ProjectileGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="proj_")
        
    def m_n_array(self, max_val):
        m = 5
        n = 1
        m_n_list = []
        while m <= max_val:
            if math.remainder(m,5) == 0 and n < m:
                m_n_list.append([m,n])
                n+=1
            elif n == m or math.remainder(m,5) != 0:
                m+=1
                if math.remainder(m,5) == 0:
                    n = 1
                    m_n_list.append([m,n])
                    n+=1
                else:
                    m_n_list.append([m,n])
        return m_n_list

    def get_difficulty_range(self, difficulty):
        if difficulty == "Easy":
            return 5
        elif difficulty == "Hard":
            return 20
        return 10

    def calculate_type1_values(self, difficulty):
        m_n_list = self.m_n_array(self.get_difficulty_range(difficulty))
        row_choice = random.randint(0, len(m_n_list)-1)
        m = m_n_list[row_choice][0]
        n = m_n_list[row_choice][1]

        v_x = m**2 - n**2
        v_y_i = 2*m*n
        v_r = m**2 + n**2
        theta = round(math.degrees(math.atan(v_y_i / v_x)), 4)
        d_x = v_x*v_y_i / 10
        d_y = v_y_i**2 / 20
        return v_x, v_r, theta, d_x, d_y

    def calculate_type2_values(self, difficulty):
        m_n_list = self.m_n_array(self.get_difficulty_range(difficulty))
        row_choice = random.randint(0, len(m_n_list)-1)
        m = m_n_list[row_choice][0]
        n = m_n_list[row_choice][1]

        v_x = m**2 - n**2
        v_y_i = 2*m*n
        v_r = m**2 + n**2
        theta = round(math.degrees(math.atan(v_y_i / v_x)), 4)
        d_x = v_x*v_y_i / 5
        d_y = v_y_i**2 / 20
        return v_r, theta, d_x, d_y
    
    def calculate_type3_low_high_values(self,difficulty):
        t_1 = random.randint(1,self.get_difficulty_range(difficulty))
        n = random.randint(1,self.get_difficulty_range(difficulty))
        m = 2*n - 1
        t_2 = t_1 + 5*m
        v_y_i = 5*(2*t_1 + t_2)
        v_x = 2*(t_1*t_2 + 25*(n-1))
        v_r = v_x + 25
        theta_i = round(math.degrees(math.atan(v_y_i / v_x)), 4)
        d_y = 5*t_1*t_2
        
        if difficulty == "Hard":
            t_x = random.randint(t_1,t_2-1) # time to base of cliff, must be after reaching height first time but before second time
        else: # easy, no setback
            t_x = t_2 #as close as possible to not landing on cliff
        
        d_x = v_x*t_x
        x_back = v_x*(t_2 - t_x) # distance from edge of cliff the object lands
        v_y_f = 5*(2*t_1 - t_2)
        theta_f = round(math.degrees(math.atan(v_y_f / v_x)), 4)
        v_f = round(((v_x**2 + v_y_f**2)**(0/5)),4)
        return t_1, t_2, v_x, v_y_i, v_r, theta_i, d_y, t_x, d_x, x_back, v_y_f, v_f, theta_f
    

    def calculate_type3_high_low_values(self,difficulty):
        m_n_list = self.m_n_array(self.get_difficulty_range(difficulty))
        row_choice = random.randint(0, len(m_n_list)-1)
        m = m_n_list[row_choice][0]
        n = m_n_list[row_choice][1]
        c = random.randint(1,difficulty)

        v_x = m**2 - n**2
        v_y_i = 2*m*n
        v_r = m**2 + n**2
        theta_i = round(math.degrees(math.atan(v_y_i / v_x)), 4)
        d_y = c*(v_y_i + 5*c)
        t = 0.2*v_y_i + c # total time
        t_level = v_y_i/5 #time to return to starting height
        if difficulty == "Hard":
            t_x = random.randint(0,t_level-1) # time for distance from edge of cliff the object is launched, must be before returning to level
            x_back = v_x*t_x # distance from the edge the the object is launched
        else: # easy, no setback
            t_x = 0
            x_back = 0

        d_x = v_x*(t-t_x) # distance from base of cliff upon landing
        v_y_f = v_y_i - 10*t
        theta_f = round(math.degrees(math.atan(v_y_f / v_x)), 4)
        v_f = round(((v_x**2 + v_y_f**2)**(0/5)),4)
        return t, t_level, v_x, v_y_i, v_r, theta_i, d_y, t_x, d_x, x_back, v_y_f, v_f, theta_f





    def generate_question(self, problem_type, difficulty):
        if problem_type == "Type 1":
            return self._generate_type1_question(difficulty)
        elif problem_type == "Type 2":
            return self._generate_type2_question(difficulty)
        else:  # Type 3
            return self._generate_type3_question(difficulty)


    def _generate_type1_question(self, difficulty):
        v_x, v_r, theta, d_x, d_y = self.calculate_type1_values(difficulty)
        object_name = random_noun()
        verb = random_proj_verb()
        
        if difficulty == "Easy":
            choice = random.randint(1,3)
            answer2 = 0
            unit2 = ""
            if choice == 1:
                question = f"If a {object_name} is {verb} horizontally off of a {d_y:.2f} m cliff with an initial velocity of {v_x:.2f} m/s, how far away does it land? (m)"
                answer = d_x
                unit = "Horizontal Distance (m)"
            elif choice == 2:
                question = f"If a {object_name} is {verb} horizontally off of a cliff at {v_x:.2f} m/s, and lands {d_x:.2f} m away, what was the height of the cliff? (m)"
                answer = d_y
                unit = "Cliff Height (m)"
            else:
                question = f"If a {object_name} is {verb} horizontally off of a {d_y:.2f} m cliff, and lands {d_x:.2f} m away, how fast was it {verb}? (m/s)"
                answer = v_x
                unit = "Initial Velocity (m/s)"
        else:  # Hard
            choice = random.randint(1,3)
            if choice == 1:
                question = f"If a {object_name} was {verb} horizontally off of a cliff and lands at {v_r:.2f} m/s at a {theta:.2f} degree angle, how fast was it {verb}, and from how high?"
                answer = v_x
                unit = "Initial Velocity (m/s)"
                answer2 = d_y
                unit2 = "Cliff Height (m)"
            elif choice == 2:
                question = f"If a {object_name} is {verb} horizontally off of a cliff at {v_x:.2f} m/s, and lands {d_x:.2f} m away, what speed and angle does it land with?"
                answer = v_r
                unit = "m/s"
                answer2 = theta
                unit2 = "degrees"
            else:
                question = f"A {object_name} is {verb} horizontally off of a {d_y:.2f} m cliff, and lands at a {theta:.2f} degree angle, with what speed did it land, and how far from the base of the cliff?"
                answer = v_r
                unit = "Overall Final Velocity (m/s)"
                answer2 = d_x
                unit2 = "Horizontal Distance (m)"
        
        return question, answer, answer2, unit, unit2

    def _generate_type2_question(self, difficulty):
        v_r, theta, d_x, d_y = self.calculate_type2_values(difficulty)
        object_name = random_noun()
        verb = random_proj_verb()
        
        if difficulty == "Easy":
            question = f"If a {object_name} is {verb} at {v_r:.2f} m/s at an angle of {theta:.2f} degrees, how far away does it land, and what is its maximum height?"
            answer = d_x
            unit = "Horizontal Distance (m)"
            answer2 = d_y
            unit2 = "Maximum Height (m)"
        else:  # Hard
            choice = random.randint(1,3)
            if choice == 1:
                question = f"A {verb} {object_name} reaches a maximum height of {d_y:.2f} m and lands {d_x:.2f} m away from where it started. What speed and angle was it launched at?"
                answer = v_r
                unit = "Initial Velocity (m/s)"
                answer2 = theta
                unit2 = "Launch Angle (degrees)"
            elif choice == 2:
                question = f"A {object_name} is {verb} at {theta:.2f} degrees, and reaches a maximum height of {d_y:.2f} m. What was its initial speed and how far away does it land?"
                answer = v_r
                unit = "m/s"
                answer2 = d_x
                unit2 = "Horizontal Distance (m)"
            else:
                question = f"A {object_name} is {verb} at {v_r:.2f} m/s, and reaches a maximum height of {d_y:.2f} m. What angle was it launched at, and how far away does it land?"
                answer = theta
                unit = "Launch Angle (degrees)"
                answer2 = d_x
                unit2 = "Horizontal Distance (m)"
        
        return question, answer, answer2, unit, unit2

    def _generate_type3_question(self, difficulty):

        object_name = random_noun()
        verb = random_proj_verb()

        direction_choice = random.randint(1,2)
        if direction_choice == 1: # high to low
            t, t_level, v_x, v_y_i, v_r, theta_i, d_y, t_x, d_x, x_back, v_y_f, v_f, theta_f = self.calculate_type3_high_low_values(difficulty)
            if difficulty == "Easy": # no setback from cliff edge
                choice = 1 #random.randint(1,3) # room for more variations
                if choice == 1:
                    question = f"""A {object_name} is {verb} off a {d_y} m high cliff at a {theta_i} degree angle 
                    at {v_r} m/s. How far away from the base of the cliff does this {object_name} land, 
                    and how fast is it moving when it hits the ground?"
                    answer = d_x
                    unit = "Horizontal Distance (m)"
                    answer2 = v_f
                    unit2 = "Final (Impact) Velocity (m/s)"""
            else: # hard: setback, add more options later
                choice = 1 #random.randint(1,3) # room for more variations
                if choice == 1:
                    question = f"A {object_name} is {verb} off a {d_y} m high cliff at {v_r} m/s at a {theta_i} 
                    degree angle. It lands {d_x} m away from the base of the cliff. How far back from the cliff's 
                    edge was it {verb}, and at what time after it was launched was it again at the height of the cliff?"
                    answer = {x_back}
                    unit = "Launch-to-cliff Distance (m)"
                    answer2 = t_level
                    unit2 = "time to return to same height (s)"

        else: # low to high
            t_1, t_2, v_x, v_y_i, v_r, theta_i, d_y, t_x, d_x, x_back, v_y_f, v_f, theta_f = self.calculate_type3_low_high_values(difficulty)
            #thing lands near edge of cliff, minimum inroad
            if difficulty == "Easy":
                choice = random.randint(1,2) # room for more variations
                if choice == 1: # give height velocity and angle, ask for distance and final angle
                    question = f"""A group of people are trying to get a {object_name} to land 
                    on top a {d_y} m high cliff. They {verb} it at {v_r} m/s at a {theta_i} degree angle. It 
                    just barely lands on the edge of the cliff. How far away from the base of the cliff was it 
                    launched from, and at what angle does it land?"""
                    answer = d_x
                    unit = "Horizontal Distance to cliff (m)"
                    answer2 = theta_f
                    unit2 = "Landing Angle (degrees)"
                elif choice == 2: # give distance velocity and angle, ask for height and final velocity
                    question = f"""A group of people are trying to get a {object_name} to land 
                    on top a cliff. They {verb} it at {v_r} m/s at a {theta_i} degree angle, {d_x} m from the 
                    base of the cliff. It just barely lands on the cliff's edge. 
                    How high up is the cliff, and what is its velocity when it lands?"""
                    answer = d_y
                    unit = "Cliff Height (m)"
                    answer2 = v_f
                    unit2 = "Landing Velocity (m/s)"
            else: # hard, setback, doesn't land on edge
                choice = 1 #random.randint(1,2) # more room for variations
                if choice == 1: # gives t_1 height and v_r to find angle, dist from edge to find dist from base
                    question = f"""A {object_name} is {verb} to get it on top of a {d_y} m cliff. 
                    It was initially {verb} at {v_r} m/s, and first reaches the cliff height after {t_1} seconds.
                    It safely lands up top, {x_back} m from the edge of the cliff.
                    What angle was it launched at, and from how far from the base of the cliff?"""
                    answer = theta_i
                    unit = "Launch Angle (degrees)"
                    answer2 = d_x
                    unti2 = "Horizontal distance from launch site to cliff face (m)"
        
        return question, answer, answer2, unit, unit2