######## A typical residential home in San Francisco, load profile
# Clean the data to align with PG&E residential tariff program
# Set-up for RESI BASELINE CHARGING
# PG&E baseline territory T

import pandas as pd
import numpy as np
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import glob
import seaborn as sns

terr = raw_input('Select Territory (T,R,W,X,S)>>> ')
file = terr+'.csv'

data = pd.read_csv(file)
#print data.head()

tcol = 'Date/Time' #time column
ecol = 'Electricity:Facility [kW](Hourly)' #total electricity col

time = list(data[tcol])
energylist = list(data[ecol])
energy = Series(energylist)
energy.name = 'energy'

monlist = [m.split(' ')[1].split('/')[0] for m in time] #month
daylist = [d.split(' ')[1].split('/')[1] for d in time]

month = Series(monlist)
month.name = 'month'
day = Series(daylist)
day.name = 'day'

######## SEASONAL
# Summer is from May1 (5/1) to Oct31 (10/31)
# Winter is Jan1 (1/1) to Apr30 (4/30)
#   and Nov 1 (11/1) to Dec 31 (12/31)

# denote summer season as 1, winter as 0

seasonlist = []
for m in monlist:
    if int(m)>=5 and int(m)<=10:
        seasonlist.append(1) #summer
    else:
        seasonlist.append(0) #winter

q = {'P':(13.8,12.3),'Q':(7,12.3),'R':(15.6,11.0),'S':(13.8,11.2),
    'T':(7.0,8.5),'V':(8.7,10.6),'W':(16.8,10.1),
    'X':(10.1,10.9),'Y':(10.6,12.6),'Z':(6.2,9.0)} # baseline quantities per territory

mincharge = 0.32854 #total daily minimum charge

tier = [0.18151,0.21546,0.27389,0.34876] # energy charge rates

######## levels
# s is baseline in summer kWh per day
sb = q[terr][0] # set summer baseline
s1 = sb*1.3 # tier 1 max (130% of baseline)
s2 = sb*2 # tier 2 max (200% of baseline)

# w is baseline in winter kWh per day
wb = q[terr][1] # set winter baseline
w1 = wb*1.3 # tier 1 max
w2 = wb*2 # tier 2 max

charge = []
usage = 0
hr = 0

eave = [] # use loop to store daily average energy usage

for i in range(len(energylist)):
    hr += 1
    usage = usage+energylist[i]
    
    if hr%24 == 0:
        eave.append(usage)
        
        if int(seasonlist[i]) == 1: #summer
            #CASE 1 under baseline
            if usage <= sb: 
                if usage*tier[0] > mincharge:
                    charge.append(usage*tier[0])
                else:
                    charge.append(mincharge)
                        
            #CASE 2 less than tier 1 more than the base
            elif usage <= s1:
                charge.append(sb*tier[0] + (usage-sb)*tier[1])
                
            #CASE 3 less than tier 2 more than tier 1
            elif usage <= s2:
                charge.append(sb*tier[0] + (s1-sb)*tier[1] + (usage-s1)*tier[2])
                
            #CASE 4 more than tier 2
            elif usage > s2:
                charge.append(sb*tier[0] + (s1-sb)*tier[1] + (s2-s1)*tier[2] +
                    (usage-s2)*tier[3])
                
            hr = 0
            usage = 0
                
        else: #winter
            #CASE 1 under baseline
            if usage <= wb: 
                if usage*tier[0] > mincharge:
                    charge.append(usage*tier[0])
                else:
                    charge.append(mincharge)
                        
            #CASE 2 less than tier 1 more than the base
            elif usage <= w1:
                charge.append(wb*tier[0] + (usage-wb)*tier[1])
                
            #CASE 3 less than tier 2 more than tier 1
            elif usage <= w2:
                charge.append(wb*tier[0] + (w1-sb)*tier[1] + (usage-w1)*tier[2])
                    
            #CASE 4 more than tier 2
            elif usage > w2:
                charge.append(wb*tier[0] + (w1-wb)*tier[1] + (w2-w1)*tier[2] +
                 (usage-w2)*tier[3])
                
            hr = 0
            usage = 0
            
total = sum(charge)         
print total
eaveser = Series(eave)
eaveser.name = 'Daily Energy Consumption, kWh'
chargeser = Series(charge)
chargeser.name = 'Daily Utility Charge, $'
basedata = pd.concat([eaveser,chargeser],axis=1)

sns.set_style("darkgrid")
basedata.plot(secondary_y=['Daily Utility Charge, $'])

plt.title('Elec Usage For Ave Home in PG&E Territory %s, E-1 rate, Annual Cost: $%d' % (terr,total))

plt.xlabel('Day of the Year')
plt.xlim(0, 356)

sns.plt.show()