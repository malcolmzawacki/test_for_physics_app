import streamlit as st

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.generators.energy_generator import EnergyGenerator
