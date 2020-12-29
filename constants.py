import os

APP_INFO = """A GUI for the pandemic simulator proposed by by [Terence S](https://terenceshin.medium.com/) in [Simulating the Pandemic in Python](https://towardsdatascience.com/simulating-the-pandemic-in-python-2aa8f7383b55)
    Change settings under the `Define scenario` menu item. Then select `Run scenario` and press `Start Simulation`.
    """
GIT_INFO = """SPS version {}. This app was implemented by [Lukas Calmbach](mailto:lcalmbach@gmail.com) using [Streamlit](https://www.streamlit.io/) and [Altair](https://altair-viz.github.io/). 
The simulation code was adapted from [Terence Shin](https://terenceshin.medium.com/).
The code can be found on [github](https://github.com/lcalmbach/pandemic-simulator)"""
MENU_LIST = ['Info', 'Define scenario', 'Run Scenario']

SETTINGS_FILENAME = os.path.join("tmp", "scenarios.json")
POPULATION_FILENAME = os.path.join("tmp", "population.json")
INFECTIONS_FILENAME = os.path.join("tmp", "infections.json")
TIMESERIES_FILENAME = os.path.join("tmp", "timeseries.json")