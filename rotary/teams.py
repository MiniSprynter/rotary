"""
teams.py

Module for collecting and storing valid team configurations.

Lawrence 23/02/22
"""


import data_tools as dt
import pandas as pd


class Teams(object):
    def __init__(self, filename=None):
        # Save parameters
        self.filename = filename

        # Load exiting data (if available)
        self.teams = self.load(filename)

    def load(self, filename):
        # Define required columns
        REQ_COLS = ["skills", "required_roles"]

        # Create empty dataframe
        data = pd.DataFrame(columns=REQ_COLS)

        # Populate dataframe (if possible)
        if filename and dt.exist(filename):
            # Load data from file
            old_data = dt.load(filename)

            # Extract data from old dataframe
            if type(old_data) is pd.DataFrame and len(old_data.index) > 0:
                # Determine valid column names
                valid_cols = [col for col in REQ_COLS
                              if col in old_data.columns]

                # Copy valid data into dataframe
                data[valid_cols] = old_data[valid_cols].copy()

        # Return populated dataframe
        return data

    def save(self, filename=None):
        # Determine filename
        if not filename:
            filename = self.filename

        # Save teams dataframe
        dt.save(self.teams, filename)
