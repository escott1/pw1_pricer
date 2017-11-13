######## FINANCIAL ANALYSIS
# A typical residential home in San Francisco, load profile
# Comparing battery simulation charges with regular TOU charges
# Finding the NPV/payback period
# PG&E baseline territory T

import pandas as pd
import numpy as np
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import glob######## FINANCIAL ANALYSIS
# A typical residential home in San Francisco, load profile
# Comparing battery simulation charges with regular TOU charges
# Finding the NPV/payback period
# PG&E baseline territory T

import pandas as pd
import numpy as np
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import glob
import matplotlib.dates as dates
import seaborn as sns
from basefun import base
from toufun import tou

######## IMPORT DATA

terr = raw_input('Select Territory (T,R,W,X,S)>>> ')

bc = base(terr) # base charge
tc = tou(terr) # tou charge


cycles = 5000
lifetime = cycles/365 #around 13 years, from the tesla website
batc = 3000 #6.4kWh cost from Tesla website
bosc = 1500 #based on SolarEdge inverter price
instc = 1000 #rough estimate
totalcost = batc+bosc+instc
dr = 0.10

ur = 1.02 #utility price escalation rate
bdr = 1.01 #battery degradation rate

npvtrack = []
yr = []
npvtrack.append(-totalcost)
yr.append(0)

npv = -totalcost
for i in range(1,lifetime+1):
    yr.append(i)
    save = bc*(ur**(i-1))-tc*(bdr**(i-1))
    npv = npv + save/((1+dr)**i)
    npvtrack.append(npv)

print npv
sns.set_style("white")
sns.barplot(yr,npvtrack,color=None, palette=None,facecolor=(0, 0, 0.1, 0.2))

plt.xlabel('Year')
plt.ylabel('Net Present Value $')
plt.title('NPV for 6.4kWh Powerwall, {0}% Discount, {1}% Utility Escalation'.format(dr*100, (ur-1)*100))
sns.plt.show()
'''
sns.set_style("darkgrid")
plt.plot(toudata, label='Regular TOU Service')
plt.plot(battdata,label='6.4kWh Powerwall on TOU Service')
plt.title('Annual Electricy For Average Home in San Francisco, PG&E E-6 TOU Service')
plt.ylabel('Daily Utility Charge, $/day')
plt.xlabel('Day of the Year')
plt.xlim(0, 356)
plt.legend()
sns.plt.show()'''
import matplotlib.dates as dates
import seaborn as sns

######## IMPORT DATA

file1 = 'toucharges.csv'
toudata = pd.read_csv(file1, index_col=0, header=None)
toudata.name = 'tou'
file2 = 'batterycharges.csv'
battdata = pd.read_csv(file2, index_col=0, header=None)

total = pd.concat([toudata, battdata], axis=1, names=['tou','bat'])
total.columns = ['tou','bat']

oldcharge = 1903.63
newcharge =  1754.30
lifetime = 13 #5000.0/365 is about 13 years, from the tesla website
batc = 3000 #7kWh cost from Tesla website
bosc = 1500 #based on SolarEdge inverter price
instc = 1000 #rough estimate
totalcost = batc+bosc+instc
dr = 0.06

ur = 1.05 #utility price escalation rate
bdr = 1.01 #battery degradation rate

npvtrack = []
yr = []
npvtrack.append(-totalcost)
yr.append(0)
npv = -totalcost
for i in range(1,lifetime+1):
    yr.append(i)
    save = oldcharge*(ur**(i-1))-newcharge*(bdr**(i-1))
    npv = npv + save/((1+dr)**i)
    npvtrack.append(npv)

print npv
sns.set_style("white")
sns.barplot(yr,npvtrack,color=None, palette=None,facecolor=(0.1, 1, 0.65, 1))

plt.xlabel('Year')
plt.ylabel('Net Present Value $')
plt.title('NPV for 6.4 kWh Tesla Powerwall, 6% Discount, 5% Utility Escalation')
sns.plt.show()
'''
sns.set_style("darkgrid")
plt.plot(toudata, label='Regular TOU Service')
plt.plot(battdata,label='6.4kWh Powerwall on TOU Service')
plt.title('Annual Electricy For Average Home in San Francisco, PG&E E-6 TOU Service')
plt.ylabel('Daily Utility Charge, $/day')
plt.xlabel('Day of the Year')
plt.xlim(0, 356)
plt.legend()
sns.plt.show()'''