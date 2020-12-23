from scipy.stats import norm
import random
import time
import streamlit as st
import altair as alt
import pandas as pd
import json


class Simulation():
    def __init__(self, scenarios: object):
        self.name = ''
        self.scenarios = scenarios
        self.num_people = 0
        self.num_elderly = 0
        self.num_midage = 0
        self.num_young = 0
        self.startingImmunity = 0
        self.startingInfecters = 0
        self.avg_days_contagious = 0
        self.lockdown_day_start = 0
        self.lockdown_day_end = 0
        self.mask_day_start = 0
        self.mask_day_end = 0
        self.mask_efficiency = 0
        self.average_friends_num = 0
        self.average_contacts_num = 0
        self.simulation_days = 0
        self.lockdown_efficiency = 0
        self.mortality_rate = 0
        self.hospitalization_rate = 0
        self.current_lockdown_factor = 0
        self.average_hospitalization_duration = 0
        self.hospital_beds_per_1k_persons = 0
        self.people_df = pd.DataFrame(columns=['index', 'starting_immunity', 'ending_immunity', 'number_infected'])
        self.std_factor = 1
        
        self.infections = []
        self.day = 0
        self.lockdown_schedule = []
        self.mask_schedule = []
        self.days = []
        self.daily_infections = 0
        self.daily_contacts = 0
        self.total_infections = 0
        self.total_contacts = 0

    def load(self): 
        setup = self.scenarios[self.name]
        
        self.startingInfecters = setup["startingInfecters"]
        self.avg_days_contagious = setup["avg_days_contagious"]
        self.lockdown_day_start = setup["lockdown_day_start"]
        self.lockdown_day_end = setup["lockdown_day_end"]
        self.lockdown_efficiency = setup["lockdown_efficiency"]
        self.mask_day_start = setup["mask_day_start"]
        self.mask_day_end = setup["mask_day_end"]
        self.mask_efficiency = setup["mask_efficiency"]
        self.average_friends_num = setup["average_friends_num"]
        self.average_contacts_num = setup["average_contacts_num"]
        self.simulation_days = setup["simulation_days"]
        self.average_contagiousness = setup["average_contagiousness"] 
        self.average_immunity = setup["average_immunity"]
        self.std_factor = setup["std_factor"]

        self.mortality_rate = setup["mortality_rate"]
        self.hospitalization_rate = setup["hospitalization_rate"]
        self.average_hospitalization_duration = setup["average_hospitalization_duration"]
        self.hospital_beds_per_1k_persons = setup["hospital_beds_per_1k_persons"]
        self.num_people = setup["num_people"]
        self.num_elderly = setup["num_elderly"]
        self.num_midage = setup["num_midage"]
        self.num_young = setup["num_young"]


    def save(self):
        setup = self.scenarios[self.name]
        setup["num_people"] = self.num_people
       
        setup["startingInfecters"] = self.startingInfecters 
        setup["avg_days_contagious"] = self.avg_days_contagious 
        setup["lockdown_day_start"] = self.lockdown_day_start 
        setup["lockdown_day_end"] = self.lockdown_day_end 
        setup["lockdown_efficiency"] = self.lockdown_efficiency 
        setup["lockdown_day_start"] = self.lockdown_day_start 
        setup["lockdown_day_start"] = self.lockdown_day_start 
        setup["mask_day_start"] = self.mask_day_start 
        setup["mask_day_end"] = self.mask_day_end 
        setup["mask_efficiency"] = self.mask_efficiency 
        setup["average_friends_num"] = self.average_friends_num 
        setup["average_contacts_num"] = self.average_contacts_num
        setup["simulation_days"] = self.simulation_days        
        setup["average_contagiousness"] = self.average_contagiousness 
        setup["average_immunity"] = self.average_immunity 
        setup["std_factor"] = self.std_factor 
        setup["avg_days_contagious"] = self.avg_days_contagious

        #setup["num_elderly"] = self.num_elderly
        #setup["num_midage"] = self.num_midage
        #setup["num_young"] = self.num_young 7
        #setup["mortality_rate"] = self.mortality_rate 
        #setup["hospitalization_rate"] = self.hospitalization_rate 
        #setup["average_hospitalization_duration"] = self.average_hospitalization_duration 
        #setup["hospital_beds_per_1k_persons"] = self.hospital_beds_per_1k_persons 
        
        with open('scenarios.json', 'wt') as myfile:
            json.dump(self.scenarios, myfile)

    def show_setting(self):
        st.write(f"num_people: {self.num_people}")
        st.write(f"startingInfecters: {self.startingInfecters}")
        st.write(f"avg_days_contagious: {self.avg_days_contagious}")
        st.write(f"mask_efficiency: {self.mask_efficiency}")
        st.write(f"average_friends_num: {self.average_friends_num}")
        st.write(f"simulation_days: {self.simulation_days}")
        st.write(f"lockdown_efficiency: {self.lockdown_efficiency}")
        st.write(f"average_contagiousness: {self.average_contagiousness}")
        st.write(f"average_immunity: {self.average_immunity}") 

    def init_schedules(self):
        """ generates a value for each day starting at set contagiousness, then dropping after 25% of days to 75%
        then increasing by 25% after 75% days. this can be used to simulate seasons. One could also simulate weekends with
        increased contacts in the young population, holidays with increased encounters among friends etc. 
        """

        self.mask_schedule = [1 for x in range(self.simulation_days)]
        self.lockdown_schedule = [1 for x in range(self.simulation_days)]
        for x in range(self.simulation_days):
            if x >= self.mask_day_start and x <= self.mask_day_end:
                self.mask_schedule[x] = 1 - (self.mask_efficiency / 100)
            if x >= self.lockdown_day_start and x <= self.lockdown_day_end:
                self.lockdown_schedule[x] = 1 - (self.lockdown_efficiency /100)
  

    def initiate_peopleDictionary(self):

        def initiate_age_groups():
            st.info('initializing elderly')
            cat_elderly = random.sample(self.peopleDictionary,self.num_elderly)
            for person in cat_elderly:
                person.age_group = 1
            st.info('initializing midage')
            cat_young_midage = list(set(self.peopleDictionary) - set(cat_elderly))
            cat_midage = random.sample(cat_young_midage,self.num_midage)
            for person in cat_midage:
                person.age_group = 2
            st.info('initializing young')
            cat_young = list(set(cat_young_midage) - set(cat_midage))    
            for person in cat_young:
                person.age_group = 3
                        
        self.peopleDictionary = []
        for x in range(0,self.num_people):
            self.peopleDictionary.append(Person(self, x))
        for person in self.peopleDictionary:
            person.init_friends()
        for x in range(0, self.startingInfecters):
            id = random.randint(0,len(self.peopleDictionary)-1)
            self.peopleDictionary[id].contagiousness = 100
        
        # initiate_age_groups()
        print('population initialized')
        print('initializing immunity')
        
    def runDay(self):
        #this section simulates the spread, so it only operates on contagious people, thus:
        for infector in [person for person in self.peopleDictionary if person.contagiousness > 0]:
            infector.make_daily_contacts()
            infector.init_contagiousness()
            for person_met in infector.contacts:                
                infector.meet(person_met)
        
        for person in [person for person in self.peopleDictionary if person.is_contagious()]:
            person.spend_sick_day()
    
    
    def run(self):  
        def generate_population_df():
            df = pd.DataFrame()
            for person in [person for person in self.peopleDictionary]:
                df=df.append(person.get_record(), ignore_index=True)
            return df

        lockdown = False
        self.init_schedules()
        self.initiate_peopleDictionary()
        st.info('Population is initialized')

        day_text = st.empty()
        plot_infections = st.empty()
        plot_r = st.empty()
        plot_fatalities = st.empty()

        df = pd.DataFrame({'day': [], 'legend': [], 'value': []})
        for x in range(1,self.simulation_days):
            self.day = x
            self.daily_infections = 0
            self.daily_contacts = 0
            #if lockdown day is reached, encounters are reduced by self.current_lockdown_factor
            if x==self.lockdown_day_start:
                self.current_lockdown_factor = (100-self.lockdown_efficiency) / 100
                
            if x == self.mask_day_start:
                for person in self.peopleDictionary:
                    person.wearMask()
            
            # infectors = 
            daily_infectors = len([person for person in self.peopleDictionary if person.is_contagious()])
            self.runDay()
            num_infected = len([person for person in self.peopleDictionary if person.is_contagious()])
            num_immune = len([person for person in self.peopleDictionary if person.immunity == 100])
            immune_pct = round((num_immune / self.num_people * 100),0)
            average_r = (self.daily_infections) / daily_infectors if daily_infectors > 0 else 0
            day_text.write(f'day {x+1}: people infected, Total infected={num_infected},{self.total_infections} immune: {num_immune} ({immune_pct}%)')
            
            data = {'day': x,'legend': 'num_infected', 'value': num_infected}
            df = df.append(data, ignore_index=True)
            data = {'day': x,'legend': 'num_immune', 'value': num_immune}
            df = df.append(data, ignore_index=True)
            data = {'day': x,'legend': 'total_infected', 'value': self.total_infections}
            df = df.append(data, ignore_index=True)
            # ratio of infected / infectors
            
            data = {'day': x,'legend': 'average_r', 'value': average_r}
            df = df.append(data, ignore_index=True)
            plot_infections.altair_chart(get_plot(df, self.simulation_days, ['num_infected','num_immune','num_infected']))
            plot_r.altair_chart(get_plot(df, self.simulation_days,['average_r']))
            if num_infected == 0:
                break
        
        df.to_csv('timeseries.csv', index = False, sep = ';') 
        pop_df = generate_population_df()
        pop_df.to_csv('population.csv', index = False, sep = ';') 
        pd.DataFrame(self.infections).to_csv('infections.csv', index = False, sep = ';') 
        

class Day():
    def __init__(self):
        self.num_contacts = 0
        self.num_infections = 0
        self.num_recoveries = 0
        self.num_fatalities=0
        self.num_hospitalisations=0

#simulation of a single person
class Person():
    def __init__(self, sim: Simulation, id: int):
        self.simulation = sim
        self.index=id
        self.immunity = 0
        self.contagious_days = 0
        self.contagiousness = 0
        self.symptoms = 0 # 0 - 10
        self.hospitalized_days = 0
        self.age_group = 1     
        self.status = 'h' #I: initial, a: active, h: hospitalized, d: dead i: isolated
        self.infection_day = 0
        self.num_of_friends = self.init_num_of_friends() 
        self.friends = []
        self.contacts = []
        self.contacts_hist = []
        self.infected_by = 0
        self.num_infected = 0
        self.num_contacts = 0
        #use gaussian distribution for number of friends; average is 5 friends
        
    def get_record(self):
        row = {'index': self.index, 'age_group':self.age_group, 'friends': self.num_of_friends, 
            'infected on date': self.infection_day, 'days contagious': self.contagious_days,
            'number of contacts': self.num_contacts, 'number of infected': self.num_infected,
            'status': self.status
            }
        return row

    def make_daily_contacts(self):
        num = norm.rvs(size=1,loc=0.5,scale=0.15)[0] * self.simulation.average_contacts_num * 2
        num = int((num * self.simulation.lockdown_schedule[self.simulation.day]).round(0))
        num = 0 if num < 0 else num
        rand_contacts = random.sample(self.simulation.peopleDictionary, num)
        # if one has only one friend he is met dayliy, otherwise you meet everyd day half of your friends

        if len(self.friends) > 1:
            num = int(round(len(self.friends) * self.simulation.lockdown_schedule[self.simulation.day], 0))
                
            friend_contacts = random.sample(self.friends, num)
        else:
            friend_contacts = self.friends

        self.contacts = friend_contacts + rand_contacts
        #self.contacts_hist.append({'day': self.simulation.day, 'contacts': self.contacts}, ignore_index=True)

    def init_num_of_friends(self):
        return int((norm.rvs(size=1,loc=0.5,scale=0.15)[0] * self.simulation.average_friends_num * 2).round(0))
    
    def accepts_friends(self):  
        return len(friends) < num_of_friends 

    def init_friends(self):
        num = self.num_of_friends - len(self.friends)
        num = 0 if num < 0 else num
        persons_accepting_friends = [person for person in self.simulation.peopleDictionary if person.accepts_friends]
        
        new_friends = random.sample(persons_accepting_friends, num)
        self.friends += new_friends
        # only for new friends
        for friend in new_friends:
            friend.friends.append(self)

    def wearMask(self):
        self.contagiousness *= self.simulation.mask_efficiency

    def init_immunity(self)-> int:
        if self.status != 'r':
            result =  int((norm.rvs(size=1,loc=self.simulation.average_immunity/100,scale=0.15)[0]*100).round(0))
            result = 0 if result < 0 else result
            self.immunity = result

    def init_contagiousness(self):
        fact = self.simulation.average_contagiousness / 100 * self.simulation.mask_schedule[self.simulation.day]
        self.contagiousness = int((norm.rvs(size=1,loc=fact,scale=0.15)[0]*100).round(0))
        

    def is_contagious(self):
        return (self.contagiousness > 0 and self.status != 'd')

    def meet(self, person: object):
        person.init_immunity()

        status = person.status
        infected = False
        if self.contagiousness > person.immunity and person.status == 'h': 
            person.init_contagiousness()
            person.infected_by = self.index
            person.infection_day = self.simulation.day
            person.status = 'a'
            self.simulation.total_infections += 1
            self.simulation.daily_infections += 1
            self.num_infected += 1
            infected = True
        else:
            infected = False
        self.num_contacts += 1
        self.simulation.daily_contacts += 1
        self.simulation.total_contacts += 1
        row = {'day': self.simulation.day, 'infector_id':self.index, 'contagiousness':self.contagiousness, 
            'contact_id': person.index, 'immunity':person.immunity, 'status before': status, 'result': infected,
            'is_lockdown_day': self.simulation.lockdown_schedule[self.simulation.day] < 1,
            'is_mask_day': self.simulation.mask_schedule[self.simulation.day] < 1,}
        self.simulation.infections.append(row)
    
    def chance_to_die(self):
        return random.randint(0,100)

    def spend_sick_day(self):
        if self.contagious_days > self.simulation.avg_days_contagious:
            self.immunity = 100
            self.contagiousness = 0
            self.status = 'r'
        else:
            self.contagious_days += 1

    #def __str__(self):
    #    return f'id: {self.index}, is contagious: {self.is_contagious}'

    #def __repr__(self):
    #    return f'Person id: {self.index}, is contagious: {self.is_contagious}'
    

class Elderly(Person):
    def __init__(self, sim: Simulation, id: int):
        super.__init__(sim, id)

class Midage(Person):
    def __init__(self, sim: Simulation, id: int):
        super.__init__(sim, id)

class Young(Person):
    def __init__(self, sim: Simulation, id: int):
        super.__init__(sim, id)

def get_plot(df, max_x: int, fields: list):
    data = df[df['legend'].isin(fields)]
    return alt.Chart(data).mark_line().encode(
        x=alt.X('day', scale=alt.Scale(domain=(0,max_x))),
        y=alt.Y('value'),
        color='legend').properties(
            width=800,
            height=400
        )

    