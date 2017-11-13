def analyze(file,life,discountrate,utilrate):
    #file = ['T'] #available territories to map 'R','W','X','S'

    from basefun import base
    from toufun import tou
    from npvfun import npv
    import timeit

    basecharge = [] # base charge
    toucharge = [] # tou charge

    bc = base(file)
    for l in range(1,life+1):
        year = l
        tc = tou(file,life,l)
    
        basecharge.append(bc)
        toucharge.append(tc)
    
    #basecharge, toucharge, cyclelife, discount rate (0.XX), utility escalate (1.0X)
    fin =  npv(basecharge,toucharge,life,discountrate,utilrate)

    return fin