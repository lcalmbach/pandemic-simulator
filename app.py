import streamlit as st
import pandemic_simulator as sim

def main():
    st.sidebar.markdown("### 🦠 Simple Pandemic Simulator")
    numPeople = st.sidebar.number_input("Population", 0,1000000, 5000)
    startingImmunity = st.sidebar.number_input("Percentage of people with natural immunity",0,100,1)
    startingInfecters =  st.sidebar.number_input("How many people will be infectious at t=0",0,int(numPeople),1)
    daysContagious =  st.sidebar.number_input("How many days contagious", 1,100,7)
    lockdownDay =  st.sidebar.number_input("Day for lockdown to be enforced", 0,200,50)
    maskDay =  st.sidebar.number_input("Day for masks to be used", 0,100,20)
    mask_efficiency_fact = st.sidebar.number_input("Masks reduces risk of infection by factor of", 0.0,1.0,0.5)
    average_contacts_num = st.sidebar.number_input("Average number of contacts",0,int(numPeople),5)
    sim_days = st.sidebar.number_input("duration of simulation in days",10,365*10,100)
    lockdown_efficiency = st.sidebar.number_input("lockdown reduces encounters by (%)", 0,100,90)
    save_scenario = st.sidebar.checkbox("Save scenario?",False)
    if save_scenario:
        scenarioid = st.sidebar.number_input("Scenario-id", 0, 100, 1)
    
    st.markdown("## Simulating the Pandemic in Python")
    st.write("""A GUI for the pandemic simulator proposed by by Terence S in [Simulating the Pandemic in Python](https://towardsdatascience.com/simulating-the-pandemic-in-python-2aa8f7383b55)
    Press start-button to start the simulation""")
    if st.button("Start simulation"):
        par_dic = {'numPeople':numPeople,
                    'startingImmunity':startingImmunity, 
                    'startingInfecters':startingInfecters, 
                    'daysContagious':daysContagious, 
                    'lockdownDay':lockdownDay, 
                    'maskDay':maskDay, 
                    'mask_efficiency_fact':mask_efficiency_fact, 
                    'average_contacts_num':average_contacts_num,
                    'sim_days':sim_days,
                    'lockdown_efficiency': lockdown_efficiency
        }
        sim.start(par_dic)

    st.sidebar.info("""A [Streamlit](https://www.streamlit.io/) GUI for the covid simulator code provided by Terence S in [Simulating the Pandemic in Python](https://towardsdatascience.com/simulating-the-pandemic-in-python-2aa8f7383b55))
            implemented by [Lukas Calmbach](mailto:lcalmbach@gmail.com).
            """)
main()
    




