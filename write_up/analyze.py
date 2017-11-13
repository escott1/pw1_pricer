from basefun import base
from toufun import tou
from npvfun import npv
import matplotlib.pyplot as plt
import seaborn as sns

f = raw_input('Enter PG&E Territory (T,R,W,X,S)>>> ')

basecharge = [] # base charge
toucharge = [] # tou charge

life = 13 #about 5000 cycles

bc = base(f)
for l in range(1,life+1):
    year = l
    tc = tou(f,life,l)
    
    basecharge.append(bc)
    toucharge.append(tc)
    print 'simulating year: {0}'.format(l)
    
#basecharge, toucharge, cyclelife, discount rate (0.XX), utility escalate (1.0X)
fin =  npv(basecharge,toucharge,life,0.07,1.05)

print 'NPV of the Powerwall project in Region %s = $%d' % (f,fin[0])

sns.set_style("white")
sns.barplot(fin[2],fin[1],color=None, palette=None,facecolor=(0.1, 0.9, 0.1, 0.85))

plt.xlabel('Year')
plt.ylabel('Net Present Value $')
plt.title('NPV for 6.4 kWh Powerwall = $%d' % (fin[0]))
sns.plt.show()




