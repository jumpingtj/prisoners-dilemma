import argparse
from . import gui
parser = argparse.ArgumentParser(description="Run GUI simulation for the Iterated Prisoner's Dilemma")
# parser.add_argument()
parser.parse_args()
gui.run_gui()