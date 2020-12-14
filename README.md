# pandemic-simulator
This simple pandemic simulator is based on an [article of S Terence](Simulating the Pandemic in Python) intruducing a simple pandemic simulator in python. It allows user input in a web interface and shows the development of infected people on the fly in a time series graph during the simulation run. Some parameters that are hard wired in Terence' model have been made interactive input. 

The following input parameters are included in this model:
- *startingImmunity* number of peolple immune from the beginning 
- *startingInfecters*': number of infected people at day 1
- *daysContagious*': number of days contagious
- *lockdownDay*': first day of lockdown
- *maskDay*': first day of wearing mask 
- *mask_efficiency_fact*': efficincy of mask for reducing contagiency 
- *average_contacts_num*': average number of friends

further input parameters have been added:
- *simulation_days*: duration of simulation, max 10 Years
- *num_people*: population size
- *lockdown_efficiency*: factor by which the daily encounters are reduced

