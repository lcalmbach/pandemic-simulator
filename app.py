import streamlit as st
from  pandemic_simulator import Simulation
import constants as cn
import json

__version__ = '0.1.0'
__author__ = 'lcalmbach@gmail.com'


def show_define_scenario_menu(sim):
    with st.beta_expander("General parameters", expanded=True):
        if sim.name == 'default':
            st.write(f"Scenario name: {sim.name}")
        else:
            sim.name = st.text_input("Scenario name", value=sim.name)
        sim.num_people = st.number_input("Population", 0,1000000, value=sim.num_people)
        sim.simulation_days = st.number_input("Duration of simulation in days",1,365*10,value = sim.simulation_days)
        #sim.hospital_beds_per_1k_persons = st.number_input("Hospital beds per 1000 persons",0.0,20.0,value=sim.hospital_beds_per_1k_persons)
        sim.average_friends_num = st.number_input("Average number of friends (daily contact)",0,int(sim.num_people),value=int(sim.average_friends_num))
        sim.average_contacts_num = st.number_input("Average number of contacts (random (contact)",0,int(sim.num_people),value=int(sim.average_contacts_num))
        sim.std_factor = st.number_input("standard deviation factor (1 = normal)",0.1,10.0, 1.0)

    #with st.beta_expander("Population", expanded=True):
    #    sim.num_elderly = st.number_input("Population age > 64",0,sim.num_people, value=sim.num_elderly)
    #    sim.num_midage = st.number_input("Population age 31 - 64",0,sim.num_people - sim.num_elderly,value=sim.num_midage)
    #    sim.num_young = sim.num_people - sim.num_elderly - sim.num_midage
    #    st.write(f'population age 0 - 30: {sim.num_young}')

    with st.beta_expander("Infection settings", expanded=True):
        sim.average_contagiousness = st.number_input("Average contagiousness (0-100)",0,100,value=sim.average_contagiousness)
        sim.average_immunity = st.number_input("average immunity (0-100)",0,100,value=sim.average_immunity)
        sim.startingInfecters =  st.number_input("How many people will be infectious at t=0",0,int(sim.num_people),value=sim.startingInfecters)
        st.write(sim.avg_days_contagious)
        sim.avg_days_contagious =  st.number_input("How many days contagious on average", 1, 100,value=sim.avg_days_contagious)
        #sim.average_hospitalization_duration = st.number_input("Average number of hospital days",0,100,value=sim.average_hospitalization_duration)
        #sim.hospitalization_rate = st.number_input("Hospitalized per 1000 infected and day",0.0,1000/sim.avg_days_contagious, value=float(sim.hospitalization_rate))
        #sim.mortality_rate = st.number_input("Mortality rate (per day and 1000 hospitalized)",0.0,1000/sim.avg_days_contagious, value=float(sim.mortality_rate))
  
    with st.beta_expander("Measures", expanded=True):
        sim.lockdown_day_start =  st.number_input("Start day for lockdown", 0,sim.simulation_days,sim.lockdown_day_start)
        sim.lockdown_day_end =  st.number_input("End day for lockdown", 0,sim.simulation_days,sim.lockdown_day_end)
        sim.lockdown_efficiency = st.number_input("lockdown reduces encounters by (%)", 0,100,50)
        sim.mask_day_start =  st.number_input("Start day for masks to be used", 0,sim.simulation_days,sim.mask_day_start)
        sim.mask_day_end =  st.number_input("End day for masks to be used", 0,sim.simulation_days,sim.mask_day_end)
        sim.mask_efficiency = st.number_input("Masks reduces risk of infection by (%))", 0,100,sim.mask_efficiency)
        
    
    sim.save()
    st.write()
    st.markdown('To create a new scenario, write the scenario name into te field below and press the `New scenario` button. ')
    new_scenario_name = st.text_input('Scenario name', '<new scenario>')
    col1, col2 = st.beta_columns([1,3])
    if col1.button("New scenario"):
        sim.scenarios[new_scenario_name] = sim.scenarios[sim.name]
        sim.save()
        sim.name = new_scenario_name
        sim.load()
    if sim.name != 'default' :
        if col2.button("Delete"):
            sim.scenarios.pop(sim.name)
            sim.name = 'default'
            sim.load()
            sim.save()
            st.experimental_rerun

def read_scenarios():
    with open('scenarios.json', 'r') as myfile:
        data=myfile.read()
        return json.loads(data)

def get_scenario_list(scenarios):
    result = []    
    for x in scenarios:
        result.append(x)
    return result


def main():
    st.sidebar.markdown("### 🦠 Simple Pandemic Simulator")
    scenarios = read_scenarios()
    list_scenarios = get_scenario_list(scenarios)
    sim = Simulation(scenarios)
    sim.name = st.sidebar.selectbox("Select a scenario", list_scenarios, index=0)
    sim.load()
    menu_item = st.sidebar.radio('Menu', cn.MENU_LIST)
    if menu_item =='Info':
        st.markdown("## Pandemic Simulator")
        st.write(cn.APP_INFO)
    elif menu_item == 'Define scenario':
        show_define_scenario_menu(sim)

    elif menu_item == 'Run Scenario':
        with st.beta_expander("Scenario settings", expanded=True):
            sim.show_setting()
        
        st.write("")
        if st.button("Start Simulation"):
            sim.run()

    st.sidebar.info(cn.GIT_INFO)
    
main()
    




