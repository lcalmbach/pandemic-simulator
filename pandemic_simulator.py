from scipy.stats import norm
import random
import time
import streamlit as st
import altair as alt
import pandas as pd

# global variables
peopleDictionary = []
lockdown = False
numPeople = 0
startingImmunity = 0 
startingInfecters = 0 
daysContagious = 0
lockdownDay = 0
maskDay = 0
mask_efficiency_fact = 0.0
average_contacts_num = 0
lockdown_efficiency = 0
lockdown_factor = 0
simulation_days = 0

#simulation of a single person
class Person():
    def __init__(self, startingImmunity, mask_efficiency_fact):
        if random.randint(0,100)<startingImmunity:
            self.immunity = True
        else:
            self.immunity = False
        self.contagiousness = 0
        self.mask = False
        self.contagiousDays = 0
        #use gaussian distribution for number of friends; average is 5 friends
        self.friends = int((norm.rvs(size=1,loc=0.5,scale=0.15)[0]*average_contacts_num*2).round(0))
        
    def wearMask(self):
        self.contagiousness *= mask_efficiency_fact
        
def initiate_peopleDictionary():
    global peopleDictionary
    peopleDictionary = []
    for x in range(0,numPeople):
        peopleDictionary.append(Person(startingImmunity, mask_efficiency_fact))
    for x in range(0,startingInfecters):
        peopleDictionary[random.randint(0,len(peopleDictionary)-1)].contagiousness = int((norm.rvs(size=1,loc=0.5,scale=0.15)[0]*10).round(0)*10)


def runDay():
    #this section simulates the spread, so it only operates on contagious people, thus:
    for person in [person for person in peopleDictionary if person.contagiousness>0 and person.friends>0]:
        peopleCouldMeetToday = int(person.friends/2)
        if peopleCouldMeetToday > 0:
            peopleMetToday = round(random.randint(0,peopleCouldMeetToday) * lockdown_factor)
        else:
            peopleMetToday = 0
            
        # if lockdown == True:
        #    peopleMetToday= 0
            
        for x in range(0,peopleMetToday):
            friendInQuestion = peopleDictionary[random.randint(0,len(peopleDictionary)-1)]
            if random.randint(0,100)<person.contagiousness and friendInQuestion.contagiousness == 0 and friendInQuestion.immunity==False:
                friendInQuestion.contagiousness = int((norm.rvs(size=1,loc=0.5,scale=0.15)[0]*10).round(0)*10)
                # print(peopleDictionary.index(person), " >>> ", peopleDictionary.index(friendInQuestion))
            
    for person in [person for person in peopleDictionary if person.contagiousness>0]:
        person.contagiousDays += 1
        if person.contagiousDays > daysContagious:
            person.immunity = True
            person.contagiousness = 0
            # print("|||", peopleDictionary.index(person), " |||")

def get_plot(df):
    return alt.Chart(df).mark_line().encode(
        x=alt.X('day', scale=alt.Scale(domain=(0,simulation_days))),
        y=alt.Y('num_infected')
    ).interactive()

def start(par_dic):  
    global lockdown          
    global numPeople
    global startingImmunity
    global startingInfecters    
    global daysContagious 
    global lockdownDay 
    global maskDay 
    global mask_efficiency_fact 
    global average_contacts_num 
    global lockdown_efficiency
    global lockdown_factor
    global simulation_days

    lockdown = False
    lockdown_factor = 1 

    numPeople = par_dic['numPeople']
    startingImmunity = par_dic['startingImmunity']
    startingInfecters = par_dic['startingInfecters']   
    daysContagious = par_dic['daysContagious']
    lockdownDay = par_dic['lockdownDay']
    maskDay = par_dic['maskDay']
    mask_efficiency_fact = par_dic['mask_efficiency_fact']
    average_contacts_num = par_dic['average_contacts_num']
    simulation_days = par_dic['sim_days']
    lockdown_efficiency = par_dic['lockdown_efficiency']
    
    day = st.empty()
    plot = st.empty()
    initiate_peopleDictionary()
    df = pd.DataFrame({'day': [], 'num_infected': []})
    for x in range(0,simulation_days):
        #if lockdown day is reached, encounters are reduced by lockdown_factor
        if x==lockdownDay:
            lockdown_factor = (100-lockdown_efficiency) / 100
            
        if x == maskDay:
            for person in peopleDictionary:
                person.wearMask()
                
        runDay()
        num = len([person for person in peopleDictionary if person.contagiousness>0])
        day.write(f'day {x+1}: people infected={num}, lockdown effectiv: {lockdown}')
        data = {'day': x,'num_infected': num}
        df = df.append(data, ignore_index=True)
        plot.altair_chart(get_plot(df))
    