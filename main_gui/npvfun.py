######## FINANCIAL ANALYSIS
# A typical residential home in San Francisco, load profile
# Comparing battery simulation charges with regular TOU charges
# Finding the NPV/payback period

# base charge, toucharge, discount rate, utility price escalator

def npv(bc,tc,lf,dr,ur):
    batc = 3000 #cost of 6.4kWh battery from Tesla website
    bosc = 1500 #inverter cost, based on SolarEdge inverter price
    instc = 1000 #install cost, rough estimate
    totalcost = batc+bosc+instc

    npvtrack = []
    yr = []
    yr.append(0)
    npvtrack.append(-totalcost)
    npv = -totalcost
    
    for i in range(1,lf+1):
        yr.append(i)
        save = bc[i-1]*(ur**(i-1))-tc[i-1]
        npv = npv + save/((1+dr)**i)
        npvtrack.append(npv)
        
    return npv, npvtrack, yr