######## A typical residential home in San Francisco, load profile
# Clean the data to align with PG&E residential tariff program
# Set-up for RESI TIME OF USE CHARGING
# PG&E baseline territory T

import pandas as pd
import numpy as np
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import glob
import seaborn as sns

dir = glob.glob('*.csv')
file = dir[0] #prints file name

data = pd.read_csv(file)
#print data.head()

tcol = 'Date/Time' #time column
ecol = 'Electricity:Facility [kW](Hourly)' #total electricity col

time = list(data[tcol])
energylist = list(data[ecol])
energy = Series(energylist)
energy.name = 'energy'

monlist = [m.split(' ')[1].split('/')[0] for m in time]
daylist = [d.split(' ')[1].split('/')[1] for d in time]
hrlist = [hr.split(' ')[3].split(':')[0] for hr in time]

######## DAY OF THE WEEK
# Start Jan 1 on a Monday
d = '01'
dow = 0
dowlist = [] 

for i in daylist:    
    if d == i:
        dowlist.append(dow)
    elif (d != i and dow < 6):
        d = i
        dow += 1
        dowlist.append(dow)
    else:
        d = i
        dow = 0
        dowlist.append(dow)

month = Series(monlist)
month.name = 'month'
day = Series(daylist)
day.name = 'day'
dow = Series(dowlist)
dow.name = 'dow'

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

######## CHARGING
# Summer and winter baselines are same as tier (7 and 8.5)
# Summer Peak (13-19) M-F (0-4)
# Summer Part-Peak (19-21), (10-13) M-F (0-4) AND (17-20) S-S (5-6)
# Summer Off-Peak (all other times)

# Winter Part-Peak (17-20) M-F (0-4)
# Winter Off-Peak (all other times)

sb = 7.0 # set summer baseline
s1 = 9.1 # tier 1 max (130% of baseline)
s2 = 14.0 # tier 2 max (200% of baseline)

# Winter (0) baseline is 8.5 kWh per day
wb = 8.5 # set winter baseline
w1 = 11.05 # tier 1 max
w2 = 17.0 # tier 2 max

metercharge = 0.25298
mincharge = 0.32854 #total daily minimum charge

sp = [0.34105,0.375,0.43254,0.50740] # summer peak rates
spp = [0.22578,0.25974,0.31727,0.39213] # summer part-peak rates
sop = [0.149,0.18297,0.24049,0.31535] # summer off-peak rates

wpp = [0.17017,0.20413,0.26166,0.33652] # winter part-peak rates
wop = [0.15334,0.1873,0.24483,0.31969] # winter off-peak rates

charge = []
usage = 0
peakuse = 0
partuse = 0
offuse = 0

eday = [] # use loop to store total daily energy usage
pu = [] #store peak usages
ppu = []
ou = []

for i in range(len(energylist)):
    if int(seasonlist[i]) == 1: #summer
    
        #during peak hours in the summer
        if (int(hrlist[i]) >= 13 and int(hrlist[i]) < 19) and (int(dowlist[i]) >= 0 and int(dowlist[i]) < 5):
            peakuse = peakuse+energylist[i]

        #partial peak hours in summer
        elif (int(hrlist[i]) >= 10 and int(hrlist[i]) < 13) and (int(dowlist[i]) >= 0 and int(dowlist[i]) < 5):
            partuse = partuse+energylist[i]
        elif (int(hrlist[i]) >= 19 and int(hrlist[i]) < 21) and (int(dowlist[i]) >= 0 and int(dowlist[i]) < 5):
            partuse = partuse+energylist[i]
        elif (int(hrlist[i]) >= 17 and int(hrlist[i]) < 20) and (int(dowlist[i]) == 5 or int(dowlist[i]) == 6):
            partuse = partuse+energylist[i]
            
        #all other timers
        else:
            offuse = offuse+energylist[i]

    else:#winter
    
        #during part peak hours in the winter
        if (int(hrlist[i]) >= 17 and int(hrlist[i]) < 20) and (int(dowlist[i]) >= 0 and int(dowlist[i]) < 5):
            partuse = partuse+energylist[i]
            
        #off-peak all other times
        else:
            offuse = offuse+energylist[i]
               
    #SUMMER
    if int(hrlist[i])%24 == 0 and int(seasonlist[i]) == 1:
        usage = peakuse+partuse+offuse
        eday.append(usage)
        pp = peakuse/usage
        ppp = partuse/usage
        opp = offuse/usage
        pu.append(pp*usage)
        ppu.append(partuse)
        ou.append(offuse)
        
        #CASE 1 under baseline
        if usage <= sb: 
            if (pp*usage*sp[0]+ppp*usage*spp[0]+opp*usage*sop[0]) > mincharge:
                charge.append(pp*usage*sp[0]+ppp*usage*spp[0]+opp*usage*sop[0]+metercharge)
            else:
                charge.append(mincharge)
                        
        #CASE 2 less than tier 1 more than the base
        elif usage <= s1:
            charge.append(pp*sb*sp[0]+ppp*sb*spp[0]+opp*sb*sop[0]+
            pp*(usage-sb)*sp[1]+ppp*(usage-sb)*spp[1]+opp*(usage-sb)*sop[1]+metercharge)
                
        #CASE 3 less than tier 2 more than tier 1
        elif usage <= s2:
            charge.append(pp*sb*sp[0]+ppp*sb*spp[0]+opp*sb*sop[0]+
            pp*(s1-sb)*sp[1]+ppp*(s1-sb)*spp[1]+opp*(s1-sb)*sop[1]+
            pp*(usage-s1)*sp[2]+ppp*(usage-s1)*spp[2]+opp*(usage-s1)*sop[2]+metercharge)
                
        #CASE 4 more than tier 2
        elif usage > s2:
            charge.append(pp*sb*sp[0]+ppp*sb*spp[0]+opp*sb*sop[0]+
            pp*(s1-sb)*sp[1]+ppp*(s1-sb)*spp[1]+opp*(s1-sb)*sop[1]+
            pp*(s2-s1)*sp[2]+ppp*(s2-s1)*spp[2]+opp*(s2-s1)*sop[2]+
            pp*(usage-s2)*sp[3]+ppp*(usage-s2)*spp[3]+opp*(usage-s2)*sop[3]+metercharge)
        
        peakuse = partuse = offuse = usage = 0
        
    #WINTER
    if int(hrlist[i])%24 == 0 and int(seasonlist[i]) == 0:
        usage = partuse+offuse
        eday.append(usage)
        ppp = partuse/usage
        opp = offuse/usage
        pu.append(0)
        ppu.append(partuse)
        ou.append(offuse)
        
        #CASE 1 under baseline
        if usage <= wb: 
            if (ppp*usage*wpp[0]+opp*usage*wop[0]) > mincharge:
                charge.append(ppp*usage*wpp[0]+opp*usage*wop[0]+metercharge)
            else:
                charge.append(mincharge)
                        
        #CASE 2 less than tier 1 more than the base
        elif usage <= w1:
            charge.append(ppp*wb*wpp[0]+opp*wb*wop[0]+
            ppp*(usage-wb)*wpp[1]+opp*(usage-wb)*wop[1]+metercharge)
                
        #CASE 3 less than tier 2 more than tier 1
        elif usage <= w2:
            charge.append(ppp*wb*wpp[0]+opp*wb*wop[0]+
            ppp*(w1-wb)*wpp[1]+opp*(w1-wb)*wop[1]+
            ppp*(usage-w1)*wpp[2]+opp*(usage-w1)*wop[2]+metercharge)
                    
        #CASE 4 more than tier 2
        elif usage > w2:
            charge.append(ppp*wb*wpp[0]+opp*wb*wop[0]+
            ppp*(w1-wb)*wpp[1]+opp*(w1-wb)*wop[1]+
            ppp*(w2-w1)*wpp[2]+opp*(w2-w1)*wop[2]+
            ppp*(usage-w2)*wpp[3]+opp*(usage-w2)*wop[3]+metercharge)
            
        peakuse = partuse = offuse = usage = 0

print max(pu)
print max(eday)
export = 0
edayser = Series(eday)
edayser.name = 'Daily Energy Consumption, kWh'
chargeser = Series(charge)

if export == 1:
    chargeser.to_csv('toucharges.csv')
    
chargeser.name = 'Daily Utility Charge, $'
basedata = pd.concat([edayser,chargeser],axis=1)


sns.set_style("darkgrid")
basedata.plot(secondary_y=['Daily Utility Charge, $'])

plt.title('Annual Electricy For Average Home in San Francisco, PG&E E-6 TOU Service, TOTAL $1956.93')
plt.xlim(0, 356)
sns.plt.show()