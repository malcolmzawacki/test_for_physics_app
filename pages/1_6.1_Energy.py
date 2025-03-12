import streamlit as st
from random import randint as ri

def get_difficulty_range(difficulty):
    if difficulty == "Easy":
        return 5
    elif difficulty == "Hard":
        return 20
    return 10

def kinetic_energy(difficulty):
     mass = ri(1,difficulty)
     velocity = ri(1,difficulty)
     flip = ri(0,1)
     if flip == 0:
          mass*=2
     else:
        velocity*=2
     return mass, velocity, 0.5*mass*velocity**2

def gravitational_potential_energy(difficulty):
    mass = ri(1,difficulty)
    height = ri(1,difficulty)
    return mass, height, mass*10*height

def elastic_potential_energy(difficulty):
     spring_constant = ri(1,difficulty)
     compression = ri(1,difficulty)
     flip = ri(0,1)
     if flip == 0:
          spring_constant*=2
     else:
        compression*=2
     return spring_constant, compression, 0.5*spring_constant*compression**2

def work(difficulty):
    force = ri(1,difficulty)
    distance = ri(1,difficulty)
    return force, distance, force*distance

def elastic_problem(difficulty):
    spring_constant, compression, elastic_e = elastic_potential_energy(difficulty)
    
    return question, answer