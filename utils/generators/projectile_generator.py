# utils/generators/projectile_generator.py
import math
import random
import sys
from pathlib import Path
#sys.path.append(str(Path(__file__).parent.parent.parent))
try:
    from .base_generator import BaseGenerator
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from utils.generators.base_generator import BaseGenerator

#from base_generator import BaseGenerator
from utils.word_lists import random_noun, random_proj_verb # does not need 

#class ProjectileGenerator(BaseGenerator):
    #def __init__(self):
        
        # Rest of your initialization code...

    # Rest of your ProjectileGenerator code...

# Add the project root directory to Python path

# Now you can import from utils
#from utils.word_lists import random_noun, random_proj_verb

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
            return 10
        elif difficulty == "Hard":
            return 50
        return 20

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
        t_x = random.randint(t_1,t_2)
        d_x = v_x*t_x
        v_y_f = 5*(2*t_1 - t_2)
        theta_f = round(math.degrees(math.atan(v_y_f / v_x)), 4)
        v_f = round(((v_x**2 + v_y_f**2)**(0/5)),4)
        return t_1, t_2, v_x, v_y_i, v_r, theta_i, d_y, t_x, d_x, v_y_f, v_f, theta_f



    def generate_question(self, problem_type, difficulty):
        if problem_type == "Type 1":
            return self._generate_type1_question(difficulty)
        else:  # Type 2
            return self._generate_type2_question(difficulty)

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