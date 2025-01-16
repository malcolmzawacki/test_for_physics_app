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

class LinearMotionGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="linear_")

    def get_difficulty_range(self, difficulty):
        if difficulty == "Easy":
            return 5
        elif difficulty == "Hard":
            return 20
        return 10

    def no_time_eq_nums(self, difficulty): # v_f,v_i,a,x 
        max_val = self.get_difficulty_range(difficulty)

        """
        changing direction is not worth scrutinizing over,
        (at least for initial launch) 
        """
        m = random.randint(3,max_val)
        if difficulty in ["Easy", "Medium"]: # v_i = 0
            n = m
            "this covers starting or ending at zero"
            """stopping (or slowing) can be handled at 
            word problem level as swapping vf, vi, a*= -1"""
        elif difficulty == "Hard":
            n = random.randint(1,m-1)
        v_i = m**2 - n**2
        v_f = m**2 + n**2
        a_x = 2* m**2 * n**2
        temp_list = []
        for i in range(2,a_x + 1):
            if a_x % i == 0:
                temp_list.append((i,a_x//i))
        list_choice = random.randint(0,len(temp_list)-1)
        a = temp_list[list_choice][0]
        x = temp_list[list_choice][1]
        return v_f,v_i,a,x
    
    def no_dist_eq_nums(self,difficulty):
        max_val = self.get_difficulty_range(difficulty)
        t = random.randint(2,max_val)
        if difficulty == "Easy":
            """easy means no initial velocity
            (or final in case of swap)"""
            v_i = 0
            a = random.randint(1,max_val)
        elif difficulty == "Medium":
            """in medium, non-zero velocities, but same dirn"""
            v_i = random.randint(1,max_val)
            a = random.randint(1,max_val)
        else: # Hard"
            """in HARD, deliberately switching direction"""
            v_i = random.randint(1,max_val)
            a = -1*random.randint((v_i//t)+1,(3*(v_i//t +2)))
            # different range of a ensures a*t is larger than v_i
            # but not unreasonably large once multiplied by t
            # somewhat balanced final velocity
            # default is v_i to right, a to left, but can be swapped
        v_f = v_i + a*t
        return v_f,v_i,a,t
    
    def no_acc_eq_nums(self,difficulty):
        max_val = self.get_difficulty_range(difficulty)
        "case of zero not currently handled here"
        "avoid by differentiating more by difficulty"
        if difficulty == "Easy":
            "so clearly, for easy, one of the velocities should be zero"
            "and the other should be positive"
            v_i = 0
            v_f = random.randint(1,max_val)
        elif difficulty == "Medium":
            "maybe both non-zero, but positive? no negatives here, no reason"
            v_i = random.randint(1,max_val)
            v_f = random.randint(v_i+1,v_i+max_val)
        else: # hard
            "change in direction, default is pos -> neg, can be swapped"
            v_i = random.randint(3,max_val)
            "need to make sure NOT equal and opposite"
            coin = random.randint(0,1)
            if coin == 0:
                v_f = -1*random.randint(1,v_i-1)
            else:
                v_f = -1*random.randint(v_i+1,v_i+max_val)
        if (v_f + v_i)%2 == 0:
            t = random.randint(2,max_val)
        else: # odd sum, needs factor of 2
            t = 2 * random.randint(1,max_val//2)
        x = (v_f + v_i)*t//2
        return x, v_f,v_i,t
    
    def no_vf_eq_nums(self,difficulty):
        max_val = self.get_difficulty_range(difficulty)
        t = random.randint(2,max_val)
        "easy: v_i = 0, a > 0"
        if t%2 == 0:
            a_mult = 1
        else:
            a_mult = 2
        if difficulty == "Easy":
            v_i = 0
            a = random.randint(1,max_val)
        elif difficulty == "Medium":
            "non-zero vi but still all positive"
            v_i = random.randint(1,max_val)
            a = random.randint(1,max_val)
        else: # hard
            "mis-matched velocity and acceleration"
            "slowed, but not reversed hmmmm"
            "2vi/t > a"
            v_i = random.randint(1,max_val)
            a = -1*random.randint(1,(2*v_i//t)+2)
        a*=a_mult # ensures divisibility if t is odd
        v_i*=a_mult # ensures directionality is preserved
        x = v_i*t + 0.5*a*t**2
        return x, v_i,t,a


    "E X T R A   S P A C E   F O R   Q U E S T I O N   F U N C T I O N S"


    def no_time_question(self, difficulty):
        """has acceleration problems, needs x, vf, vi"""
        noun = random_noun()
        coin = random.randint(0,1)  # determines speeding up or slowing down
        var_dice = random.randint(0, 3)  # roll for variable to solve for
        v_f, v_i, a, x = self.no_time_eq_nums(difficulty)
        if coin == 0:
            verb = "speeds up"
        else:
            a *= -1
            verb = "slows down"

        if difficulty in ["Easy", "Medium"]:
            if var_dice == 0:  # Solve for acceleration
                unit = "m/s²"
                answer = a
                if verb == "speeds up":
                    question = f"""What acceleration would a {noun} at rest need to experience \
                    for it to reach a velocity of {v_f} m/s over a distance of {x} meters?"""
                else:
                    question = f"""How much deceleration would a {noun} moving at {v_f} m/s \
                    need in order to come to rest over a distance of {x} meters?"""
            elif var_dice in [1,2]:  # Solve for final velocity, swap for 'initial' if slowing
                unit = "m/s"
                answer = v_f
                if verb == "speeds up":
                    question = f"""If a {noun} starts from rest and accelerates at {a} m/s² \
                    over a distance of {x} meters, what velocity does it reach?"""
                else:
                    question = f"""If a {noun} decelerates at {-1*a} m/s² to rest \
                    over {x} meters, what was its initial velocity?"""
            elif var_dice == 3:  # Solve for distance
                unit = "meters"
                answer = x
                if verb == "speeds up":
                    question = f"""A {noun} at rest accelerates at {a} m/s² to a velocity of {v_f} m/s. \
                    How far did it travel during this time?"""
                else:
                    question = f"""A {noun} decelerates at {-1*a} m/s² from {v_f} m/s to rest. \
                    How far did it travel during this time?"""
        else:  # HARD difficulty
            if var_dice == 0:  # Solve for acceleration
                unit = "m/s²"
                answer = a
                if verb == "speeds up":
                    question = f"""What acceleration would a {noun} moving at {v_i} m/s need to experience \
                    for it to speed up to {v_f} m/s over a distance of {x} meters?"""
                else:
                    question = f"""What deceleration would a {noun} moving at {v_f} m/s need to experience \
                    to slow down to {v_i} m/s over a distance of {x} meters?"""
            elif var_dice == 1:  # Solve for final velocity
                unit = "m/s"
                answer = v_f
                if verb == "speeds up":
                    question = f"""If a {noun} starts at {v_i} m/s and accelerates at {a} m/s² \
                    over {x} meters, what velocity does it reach?"""
                else:
                    question = f"""If a {noun} decelerates at {-1*a} m/s² from {v_f} m/s \
                    to {v_i} m/s over {x} meters, what is the final velocity?"""
            elif var_dice == 2:  # Solve for initial velocity
                unit = "m/s"
                answer = v_i
                if verb == "speeds up":
                    question = f"""If a {noun} accelerates at {a} m/s² to {v_f} m/s \
                    over {x} meters, what was its initial velocity?"""
                else:
                    question = f"""If a {noun} decelerates at {-1*a} m/s² to {v_f} m/s \
                    over {x} meters, what was its initial velocity?"""
            elif var_dice == 3:  # Solve for distance
                unit = "meters"
                answer = x
                if verb == "speeds up":
                    question = f"""A {noun} accelerates from {v_i} m/s to {v_f} m/s at {a} m/s². \
                    How far did it travel?"""
                else:
                    question = f"""A {noun} decelerates from {v_f} m/s to {v_i} m/s at {-1*a} m/s². \
                    How far did it travel?"""

        return question, answer, unit
            
    "Formatting on HARD here could be improved to state direction textually. still includes negative signs. gotta ship something tho"
    def no_dist_question(self, difficulty):
        """has a, needs t, vf, vi"""
        v_f, v_i, a, t = self.no_dist_eq_nums(difficulty)
        noun = random_noun()
        coin = random.randint(0, 1)  # determines speeding up or slowing down
        var_dice = random.randint(0, 3)  # roll for variable to solve for
        if coin == 0:
            verb = "speeds up"
        else:
            a *= -1
            verb = "slows down"
        if difficulty == "Easy":
            if var_dice == 0:  # Solve for acceleration
                unit = "m/s²"
                answer = a
                if coin == 0: # speeding up
                    question = f"""What acceleration would a {noun} initially at rest need to \
                    experience to get to {v_f} m/s in {t} seconds?"""
                else: # slowing down
                    question = f"""What deceleration would a {noun} initally moving at {v_f} m/s need to \
                    experience to get to rest in {t} seconds?"""
            elif var_dice in [1,2]:  # Solve for final velocity since initial is zero in easy
                unit = "m/s"
                answer = v_f
                if coin == 0:
                    question = f"""If a {noun} starts at rest and accelerates at {a} m/s² for \
                    {t} seconds, what velocity does it reach?"""
                else:
                    question = f"""If a {noun} decelerates at {-1*a} m/s² for \
                    {t} seconds in order to come to rest, what velocity did it start with?"""
            elif var_dice == 3:  # Solve for time
                unit = "seconds"
                answer = t
                if coin == 0: #speeding up
                    question = f"""A {noun} accelerates from rest at {a} m/s², reaching {v_f} m/s. \
                    How long does it take?"""
                else:
                    question = f"""A {noun} decelerates from {v_f} m/s to rest at a rate of {-1*a}  m/s². \
                    How long does it take?"""
        elif difficulty == "Medium":
            if var_dice == 0:  # Solve for acceleration
                unit = "m/s²"
                answer = a
                if coin == 0:
                    question = f"""Determine the acceleration required for a {noun} moving at {v_i} m/s \
                    to speed up to {v_f} m/s in {t} seconds."""
                else:
                    question = f"""Determine the deceleration required for a {noun} moving at {v_f} m/s \
                    to slow to {v_i} m/s in {t} seconds."""
            elif var_dice in [1,2]:  # Solve for final velocity, they are reversible
                unit = "m/s"
                answer = v_f
                if coin == 0:
                    question = f"""A {noun} starts at {v_i} m/s and accelerates at {a} m/s² for {t} seconds. \
                    What is its final velocity?"""
                else:
                    question = f"""A {noun} slows to {v_i} m/s after decelerating at {-1*a} m/s² for {t} seconds. \
                    What was its initial velocity?"""
            elif var_dice == 3:  # Solve for time
                unit = "seconds"
                answer = t
                if coin == 0:
                    question = f"""A {noun} accelerates from {v_i} m/s to {v_f} m/s with an acceleration of {a} m/s². \
                    How much time does it take?"""
                else:
                    question = f"""A {noun} decelerates from {v_f} m/s to {v_i} m/s at a rate of {a} m/s². \
                    How much time does it take?"""
        else:  # HARD difficulty
            if var_dice == 0:  # Solve for acceleration
                unit = "m/s²"
                answer = a
                question = f"""What acceleration would a {noun} moving at {v_i} m/s need to experience \
                to {verb} to {v_f} m/s in {t} seconds?"""
            elif var_dice == 1:  # Solve for final velocity
                unit = "m/s"
                answer = v_f
                question = f"""If a {noun} starts at {v_i} m/s and {verb} at {a} m/s² for {t} seconds, \
                what velocity does it reach?"""
            elif var_dice == 2:  # Solve for initial velocity
                unit = "m/s"
                answer = v_i
                question = f"""If a {noun} {verb} at {a} m/s² to reach {v_f} m/s in {t} seconds, \
                what was its initial velocity?"""
            elif var_dice == 3:  # Solve for time
                unit = "seconds"
                answer = t
                question = f"""A {noun} {verb} at {a} m/s² from {v_i} m/s to {v_f} m/s. \
                How long does it take?"""

        return question, answer, unit

    
    def no_acc_question(self,difficulty):
        "has t,x, needs vf, vi"
        x, v_f,v_i,t = self.no_acc_eq_nums(difficulty)
        noun = random_noun()
        coin = random.randint(0,1)
        var_dice = random.randint(0,1)
        if difficulty == "Easy":
            "so clearly, for easy, one of the velocities should be zero"
            "and the other should be positive. default is speeding up"
            if var_dice == 0: # time
                unit = "seconds"
                answer = t
                if coin == 0: # speeding up
                    question = f"""A {noun} initially at rest accelerates at a constant rate over a distance of {x} meters. 
                    If it reached a velocity of {v_f} m/s, how much time did it take to get up to that speed?"""
                else:
                    question = f"""A {noun} initially moving at a velocity of {v_f} m/s decelerates at a constant rate 
                    until it is at a full stop. If this occurred over a distance of {x} meters, how much time did it take?"""
            elif var_dice == 1: # x
                unit = "meters"
                answer = x
                if coin == 0: # speeding up
                    question = f"""A {noun} initially at rest accelerates at a constant rate for {t} seconds. 
                    If it reached a velocity of {v_f} m/s, how much distance did it cover during that time?"""
                else:
                    question = f"""A {noun} initially moving at a velocity of {v_f} m/s decelerates at a constant rate 
                    until it is at a full stop. If this occurred over {t} seconds, how much distance did it cover?"""
            elif var_dice in [2,3]: # velocity, reversible
                unit = "m/s"
                answer = v_f
                if coin == 0: # speeding up
                    question = f"""A {noun} initially at rest accelerates at a constant rate for {t} seconds. \
                    If this occurred over {x} meters, what velocity did the {noun} reach?"""
                else:
                    question = f"""A noun reaches rest after decelerating at a constant rate for {t} seconds. \ 
                    If this occurred over {x} meters, what velocity did {noun} start with?"""

        elif difficulty == "Medium":
            "maybe both non-zero, but positive? no negatives here, no reason"
            if var_dice == 0: # time
                unit = "seconds"
                answer = t
                if coin == 0: # speeding up
                    question = f"""A {noun} initially moving at {v_i} m/s accelerates at a constant rate over a distance of {x} meters. 
                    If it reaches a final velocity of {v_f} m/s, how much time did it take to get up to that speed?"""
                else:
                    question = f"""A {noun} initially moving at a velocity of {v_f} m/s decelerates at a constant rate 
                    until it is at a new velocity of {v_i} m/s. If this occurred over a distance of {x} meters, how much time did it take?"""
            elif var_dice == 1: # x
                unit = "meters"
                answer = x
                if coin == 0: # speeding up
                    question = f"""A {noun} initially moving at {v_i} m/s accelerates at a constant rate for {t} seconds. 
                    If it reaches a final velocity of {v_f} m/s, how much distance did it cover during that time?"""
                else:
                    question = f"""A {noun} initially moving at a velocity of {v_f} m/s decelerates at a constant rate 
                    until it is at a new velocity of {v_i} m/s. If this occurred over {t} seconds, how much distance did it cover?"""
            elif var_dice in [2,3]: # v_f,vi
                unit = "m/s"
                if coin == 0:
                    answer = v_f
                    question = f"""A {noun} initially moving at {v_i} m/s accelerates at a constant rate for {t} seconds.\
                        If this occurred over a distance of {x} meters, what velocity did it reach?"""
                else:
                    answer = v_i
                    question = f"""A {noun} initially moving at {v_f} m/s decelerates at a constant rate for {t} seconds.\
                        If this occurred over a distance of {x} meters, what velocity did it reach?"""
            
        else: # hard
            "change in direction, default is pos -> neg, can be swapped"
            if x > 0:
                direction_phrase = "to the right"
            else:
                direction_phrase = "to the left"
            if var_dice == 0: # time
                unit = "seconds"
                answer = t
                if coin == 0: # vi>0, vf<0
                    question = f"""A {noun}, initially moving at {v_i} m/s to the right, slows all the way down,
                    and gets back up to {-1*v_f} m/s to the left. 
                    The {noun} travels {abs(x)} meters {direction_phrase} in the process. 
                    How much time did this take?"""
                else: # vi<0, a>0
                    question = f"""A {noun}, initially moving at {-1*v_f} m/s to the left, 
                    slows all the way down, and gets back up to {v_i} m/s to the right.  
                    The {noun} travels {abs(x)} meters {direction_phrase} in the process. 
                    How much time did this take?"""
            elif var_dice == 1: # x
                unit = "meters"
                answer = x
                if coin == 0: # vi>0, vf<0
                    question = f"""A {noun}, initially moving at {v_i} m/s to the right,  
                    slows all the way down, and gets back up to {-1*v_f} m/s to the left in {t} seconds.  
                    What is the {noun}'s displacement?"""
                else: # vi<0, a>0
                    question = f"""A {noun}, initially moving at {-1*v_f} m/s to the left,  
                    slows all the way down, and gets back up to {v_i} m/s to the right in {t} seconds.  
                    What is the {noun}'s displacement?"""
            elif var_dice in [2,3]:
                unit = "m/s"
                if coin == 0:
                    answer = v_f
                    question = f"""A {noun}, initially moving at {v_i} m/s to the right, experiences a constant acceleration that 
                    slows it all the way down, and speeds it back up to the left. 
                    The acceleration was applied for {t} seconds, and resulted in the {noun} 
                    traveling {abs(x)} meters {direction_phrase}.
                    What is the final velocity of the {noun}?"""
                else:
                    answer = v_i
                    question = f"""A {noun}, initially moving at {-1*v_f} m/s to the left, experiences a constant acceleration that 
                    slows it all the way down, and speeds it back up to the right. 
                    The acceleration was applied for {t} seconds, and resulted in the {noun} 
                    traveling {abs(x)} meters {direction_phrase}.
                    What is the final velocity of the {noun}?"""

        return question, answer, unit
    
    def no_vf_question(self,difficulty):
        "has x, needs a, vi, t -> (for easy, hard only)"
        x, v_i,t,a = self.no_vf_eq_nums(difficulty)
        noun = random_noun()
        if difficulty == "Easy":
            "vi = 0, find only x a t"
            var_dice = random.randint(0,2)
            if var_dice == 0: # x
                question = f"""A {noun}, initially at rest, accelerates at a rate of {a} m/s² for {t} seconds.
                How far does it go during this time?"""
                answer = x
                unit = "meters"
            elif var_dice == 1: # time
                answer = t
                unit = "seconds"
                question = f"""A {noun}, initially at rest, accelerates at a rate of {a} m/s² over {x} meters.
                How long does this take?"""
            else:
                answer = a
                unit = "m/s²"
                question = f"""A {noun}, initially at rest, accelerates at a constant rate for {t} seconds over {x} meters.
                How big was the acceleration?"""
        elif difficulty == "Medium":
            "non-zero vi but still all positive. find x , vi, a (NOT t)"
            var_dice = random.randint(0,2)
            if var_dice == 0: # x
                question = f"""A {noun}, initially moving at {v_i} m/s, accelerates at a rate of {a} m/s² for {t} seconds.
                How far does it go during this time?"""
                answer = x
                unit = "meters"
            elif var_dice == 1: # vi
                question = f"""A {noun}, initially moving to the right, accelerates at a rate of {a} m/s² for {t} seconds.
                The {noun} covers {x} meters. How fast was it initially moving?"""
                answer = v_i
                unit = "m/s"
            else: # a
                answer = a
                unit = "m/s²"
                question = f"""A {noun}, initially moving at {v_i} m/s, accelerates at a constant rate for {t} seconds over {x} meters.
                How big was the acceleration?"""
        else: # hard
            "mis-matched velocity and acceleration, sometimes?? somehow re-loop in medium?"
            "one in three chance, maybe"
            medium_chance = random.randint(0,2)
            if medium_chance == 0:
                question, answer, unit = self.no_vf_question(difficulty)
            else:
                "find all four"
                var_dice = random.randint(0,3)
                if var_dice == 0: # x
                    question = f"""A {noun} is initially moving at {v_i} m/s to the right, 
                    but is slowed by an acceleration of {-1*a} m/s² for {t} seconds.
                    How far does it go during this time?"""
                    answer = x
                    unit = "meters"
                elif var_dice == 1: #v_i
                    question = f"""A {noun}, initially moving to the right, is slowed at a rate of {-1*a} m/s² for {t} seconds.
                    Despite this, {noun} covers {x} meters. How fast was it initially moving?"""
                    answer = v_i
                    unit = "m/s"
                elif var_dice == 2: # a
                    answer = a
                    unit = "m/s²"
                    question = f"""A {noun}, initially moving at {v_i} m/s to the right, is slowed at a constant rate for {t} seconds over {x} meters.
                    What was the acceleration?"""
                else: # time
                    answer = t
                    unit = "seconds"
                    question = f"""A {noun}, initially moving at {v_i} m/s to the right, is slowed at a constant rate {-1*a} m/s².
                    How much time does this take for the {noun} to cover {x} meters?"""



        return question, answer, unit
    
    def mixed_question(self,difficulty):
        dice = random.randint(0,3)
        if dice == 0:
            question, answer, unit = self.no_time_question(difficulty)
        elif dice == 1:
            question, answer, unit = self.no_dist_question(difficulty)
        elif dice == 2:
            question, answer, unit = self.no_acc_question(difficulty)
        else:
            if difficulty == "Hard":
                coin = random.randint(0,1)
                if coin == 0:
                    question, answer, unit = self.no_vf_question("Medium")
                else:
                    question, answer, unit = self.no_vf_question(difficulty)
            else:
                question, answer, unit = self.no_vf_question(difficulty)

        return question, answer, unit