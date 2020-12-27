from scipy.stats import norm
import random
import time
import streamlit as st
import altair as alt
import pandas as pd
import json
import constants as cn


class Simulation():
    def __init__(self, scenarios: object):
        self.name = ''
        self.scenarios = scenarios
        self.num_people = 0
        self.num_elderly = 0
        self.num_midage = 0
        self.num_young = 0
        self.startingInfecters = 0
        self.avg_days_contagious = 0
        self.lockdown_day_start = 0
        self.lockdown_day_end = 0
        self.mask_day_start = 0
        self.mask_day_end = 0
        self.mask_efficiency = 0
        self.avg_friends_num = 0
        self.avg_contacts_num = 0
        self.avg_chance_infection = 0
        self.simulation_days = 0
        self.lockdown_efficiency = 0
        self.mortality_rate = 0
        self.hospitalization_rate = 0
        self.current_lockdown_factor = 0
        self.avg_hospitalization_duration = 0
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
        
        self.num_people = setup["num_people"]
        self.startingInfecters = setup["startingInfecters"]
        self.avg_days_contagious = setup["avg_days_contagious"]
        self.lockdown_day_start = setup["lockdown_day_start"]
        self.lockdown_day_end = setup["lockdown_day_end"]
        self.lockdown_efficiency = setup["lockdown_efficiency"]
        self.mask_day_start = setup["mask_day_start"]
        self.mask_day_end = setup["mask_day_end"]
        self.mask_efficiency = setup["mask_efficiency"]
        self.avg_friends_num = setup["avg_friends_num"]
        self.avg_contacts_num = setup["avg_contacts_num"]
        self.simulation_days = setup["simulation_days"]
        self.avg_chance_infection = setup["avg_chance_infection"] 
        self.std_factor = setup["std_factor"]

        self.mortality_rate = setup["mortality_rate"]
        self.hospitalization_rate = setup["hospitalization_rate"]
        self.avg_hospitalization_duration = setup["avg_hospitalization_duration"]
        self.hospital_beds_per_1k_persons = setup["hospital_beds_per_1k_persons"]
        
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
        setup["avg_friends_num"] = self.avg_friends_num 
        setup["avg_contacts_num"] = self.avg_contacts_num
        setup["simulation_days"] = self.simulation_days        
        setup["avg_chance_infection"] = self.avg_chance_infection 
        setup["std_factor"] = self.std_factor 
        setup["avg_days_contagious"] = self.avg_days_contagious

        #setup["num_elderly"] = self.num_elderly
        #setup["num_midage"] = self.num_midage
        #setup["num_young"] = self.num_young 7
        #setup["mortality_rate"] = self.mortality_rate 
        #setup["hospitalization_rate"] = self.hospitalization_rate 
        #setup["avg_hospitalization_duration"] = self.avg_hospitalization_duration 
        #setup["hospital_beds_per_1k_persons"] = self.hospital_beds_per_1k_persons 
        
        with open(cn.SETTINGS_FILENAME, 'wt') as myfile:
            json.dump(self.scenarios, myfile)
            close()

    def show_setting(self):
        st.write(f"Population: {self.num_people}")
        st.write(f"Simulation days: {self.simulation_days}")
        st.write(f"Number of infected persons at t=0: {self.startingInfecters}")
        st.write(f"Average days of contagiousness: {self.avg_days_contagious}")
        st.write(f"Average number of friends: {self.avg_friends_num}")
        st.write(f"Average number of random contacts: {self.avg_contacts_num}")
        st.write(f"Average probability of infection per contact: {self.avg_chance_infection}")
        st.write(f"Lockdown: from day {self.lockdown_day_start} to day {self.lockdown_day_end}")
        st.write(f"Lockdown reduces contacts by {self.lockdown_efficiency}%")
        st.write(f"Mask mandatory from day {self.mask_day_start} to day {self.mask_day_end}")
        st.write(f"Masks reduce risk of contagion by {self.mask_efficiency}%")


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
  
    @st.cache
    def initiate_peopleDictionary(self):

        def initiate_age_groups():
            cat_elderly = random.sample(self.peopleDictionary,self.num_elderly)
            for person in cat_elderly:
                person.age_group = 1
            cat_young_midage = list(set(self.peopleDictionary) - set(cat_elderly))
            cat_midage = random.sample(cat_young_midage,self.num_midage)
            for person in cat_midage:
                person.age_group = 2
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
            self.peopleDictionary[id].status = 'a'
        
        # initiate_age_groups()
        print('population initialized')
        
    def runDay(self):
        #this section simulates the spread, so it only operates on contagious people, thus:
        all_contacts = []
        for infector in [person for person in self.peopleDictionary if person.is_contagious()]:
            all_contacts += infector.get_daily_contacts()
        
        # contacts taht result in an infection:
        factor = self.avg_chance_infection * self.lockdown_schedule[self.day] * self.mask_schedule[self.day]
        infections = random.sample(all_contacts, int(round(len(all_contacts) * factor / 100, 0)))
        for infection in infections:     
            infection['infector'].infect(infection['infected'])
        
        for contagious_person in [person for person in self.peopleDictionary if person.is_contagious()]:
            contagious_person.spend_sick_day()
    
    
    def run(self):  
        def generate_population_df():
            df = pd.DataFrame()
            for person in [person for person in self.peopleDictionary]:
                df=df.append(person.get_record(), ignore_index=True)
            return df

        self.init_schedules()
        self.initiate_peopleDictionary()
        st.info('Population is initialized')

        day_text = st.empty()
        plot_infections = st.empty()
        plot_r = st.empty()
        plot_fatalities = st.empty()
        num_infected_last_week = 0
        num_infected_last_week = 0
        avg_r = 0

        df = pd.DataFrame({'day': [], 'legend': [], 'cases': []})
        for x in range(1,self.simulation_days):
            self.day = x
            self.daily_infections = 0
            self.daily_contacts = 0
            #if lockdown day is reached, encounters are reduced by self.current_lockdown_factor
            if x==self.lockdown_day_start:
                self.current_lockdown_factor = (100-self.lockdown_efficiency) / 100
                            
            # infectors = 
            daily_infectors = len([person for person in self.peopleDictionary if person.is_contagious()])
            self.runDay()
            if self.day >= 7:
                infectors_1week_ago = [person for person in self.peopleDictionary if person.infection_day == self.day - 7]
                num_infections_last_week = len([person for person in self.peopleDictionary if person.infected_by in infectors_1week_ago]) 
                avg_r = num_infections_last_week / len(infectors_1week_ago) if len(infectors_1week_ago) != 0 else 0
            num_infected = len([person for person in self.peopleDictionary if person.is_contagious()]) 
            num_immune = len([person for person in self.peopleDictionary if person.status == 'r'])
            immune_pct = round((num_immune / self.num_people * 100),0)
            
            day_text.write(f'day {x+1}: people infected, Total infected={num_infected},{self.total_infections} immune: {num_immune} ({immune_pct}%)')
            
            data = {'day': x,'legend': 'num_infected', 'cases': num_infected}
            df = df.append(data, ignore_index=True)
            data = {'day': x,'legend': 'num_immune', 'cases': num_immune}
            df = df.append(data, ignore_index=True)
            data = {'day': x,'legend': 'total_infected', 'cases': self.total_infections}
            df = df.append(data, ignore_index=True)
            # ratio of infected / infectors
            
            data = {'day': x,'legend': 'avg_r', 'cases': avg_r}
            df = df.append(data, ignore_index=True)
            plot_infections.altair_chart(get_plot(df, self.simulation_days, ['num_infected','num_immune','num_infected']))
            plot_r.altair_chart(get_plot(df, self.simulation_days,['avg_r']))
            if num_infected == 0:
                break
        
        df.to_csv(cn.TIMESERIES_FILENAME, index = False, sep = ';') 
        generate_population_df().to_csv(cn.POPULATION_FILENAME, index = False, sep = ';') 
        pd.DataFrame(self.infections).to_csv(cn.INFECTIONS_FILENAME, index = False, sep = ';') 
        

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
        self.contagious_days = 0
        self.symptoms = 0 # 0 - 10
        self.hospitalized_days = 0
        self.age_group = 1     
        self.status = 'h' #I: initial, a: active, h: hospitalized, d: dead i: isolated
        self.infection_day = -99
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

    def get_daily_contacts(self):
        num = norm.rvs(size=1,loc=0.5,scale=0.15)[0] * self.simulation.avg_contacts_num * 2
        num = int((num * self.simulation.lockdown_schedule[self.simulation.day]).round(0))
        num = 0 if num < 0 else num
        rand_contacts = random.sample(self.simulation.peopleDictionary, num)
        # if one has only one friend he is met dayliy, otherwise you meet everyd day half of your friends
        result = []
        for person in self.friends:
            result.append({'infector': self, 'infected': person})
        for person in rand_contacts:
            result.append({'infector': self, 'infected': person})
        return result

    def init_num_of_friends(self):
        return int((norm.rvs(size=1,loc=0.5,scale=0.15)[0] * self.simulation.avg_friends_num * 2).round(0))
    
    def accepts_friends(self): 
        """
        Accept friends if you habe less than 3 * avg_friends_num
        """
        return len(self.friends) < self.simulation.avg_friends_num * 3

    def init_friends(self):
        num = self.num_of_friends - len(self.friends)
        num = 0 if num < 0 else num
        persons_accepting_friends = [person for person in self.simulation.peopleDictionary if person.accepts_friends()]
        self.friends = random.sample(persons_accepting_friends, num)
        # only for new friends
        for friend in self.friends:
            if friend.index != self.index:
                friend.friends.append(self)


    def is_contagious(self):
        return (self.status == 'a')

    def infect(self, person: object):
        has_infected = False
        if person.status == 'h': 
            person.infection_day = self.simulation.day
            person.status = 'a'
            person.infected_by = self
            has_infected = True
            self.simulation.daily_infections += 1
            self.simulation.total_infections +=1
        self.num_contacts += 1
        row = {'day': self.simulation.day, 'infector_id':self.index, 
            'contact_id': person.index,
            'is_lockdown_day': self.simulation.lockdown_schedule[self.simulation.day] < 1,
            'is_mask_day': self.simulation.mask_schedule[self.simulation.day] < 1,
            'has infected': has_infected,
            }
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
        y=alt.Y('cases'),
        color='legend').properties(
            width=800,
            height=400
        )

    