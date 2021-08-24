import time
import numpy as np
import pandas as pd
from knapsackOptimisation import expectedZn, Zn_data

# Set Cover problem with cost and efficacy constraint
def setCoverCostEfficacy(sets,universe,budget,weights,efficacy,efficacy_bound):
    def setCover(sets,set_reminder,budget,weights,efficacy,efficacy_bound):
        min_element = -1
        for i,s in enumerate(sets):
            if len(s.intersection(set_reminder)) > 0:
                try:
                    cost = weights[i]/(len(s.intersection(set_reminder)))
                    if cost <= budget and all(j >= efficacy_bound for j in efficacy[i]):
                        budget = cost
                        min_element = i
                except:
                    pass
        return(sets[min_element],weights[min_element],min_element)

    cover = []
    costs = []
    pos = []
    timeout = time.time() + 60*0.2  # 6 seconds from now
    set_reminder = universe
    while len(set_reminder) != 0 and budget != 0:
        if time.time() > timeout:
            break
        set_i, cost_i, loc = setCover(sets,set_reminder,budget,weights,efficacy,efficacy_bound)
        if loc != -1:
            cover.append(set_i)
            set_reminder = set_reminder.difference(set_i)
            costs.append(cost_i)
            pos.append(loc)
            budget = budget - cost_i
        time.sleep(1)

    res = [i for set_i in cover for i in set_i]
    # print(f'cover:{cover}')
    # print(f'res:{np.unique(res)}')

    if len(np.unique(res)) == len(universe):
        print(f'SCCE: cover={cover}---{sum(costs)},{costs}----{pos}')
        return(cover,costs,pos)
    else:
        print('No cover')
        return([],[],[])


# Set Cover with cost constraint
def setCoverCost(sets,universe,budget,weights):
    def setCover(sets,set_reminder,budget,weights):
        min_element = -1
        for i,s in enumerate(sets):
            if len(s.intersection(set_reminder)) > 0:
                try:
                    cost = weights[i]/(len(s.intersection(set_reminder)))
                    if cost <= budget:
                        budget = cost
                        min_element = i
                except:
                    pass
        return(sets[min_element],weights[min_element],min_element)

    cover = []
    costs = []
    pos = []
    timeout = time.time() + 60*0.2  # 6 seconds from now
    set_reminder = universe
    while len(set_reminder) != 0 and budget != 0:
        if time.time() > timeout:
            break
        set_i, cost_i, loc = setCover(sets,set_reminder,budget,weights)
        if loc != -1:
            cover.append(set_i)
            set_reminder = set_reminder.difference(set_i)
            costs.append(cost_i)
            pos.append(loc)
            budget = budget - cost_i
        time.sleep(1)

    res = [i for set_i in cover for i in set_i]

    if len(np.unique(res)) == len(universe):
        print(f'SCC: cover={cover}---{sum(costs)},{costs}----{pos}')
        return(cover,costs,pos)
    else:
        print('No cover')
        return([],[],[])

# Set Cover Problem with No Constraint
def setCover(sets,universe,costH):
    set_reminder = universe
    cover = []
    pos = []
    list_len = [len(i) for i in sets]
    max_pos = list_len.index(max(list_len))
    pos.append(max_pos)
    set_reminder = set_reminder.difference(sets[max_pos])
    cover.append(sets[max_pos])
    while len(set_reminder) != 0:
        temp = [len(s.intersection(set_reminder)) for s in sets]
        ele = [[sets[i],i] for i,e in enumerate(temp) if e!= 0]
        elements = [i[0] for i in ele]
        min_set = min(elements, key=len)
        ind = elements.index(min_set)
        pos.append(ele[ind][1])
        cover.append(min_set)
        set_reminder = set_reminder.difference(min_set)
    print(f'SC: cover={cover}---pos={pos}')
    costs = [costH[i] for i in pos]
    return(cover,costs,pos)

# Set Cover Problem risk (E[Zn]) calculation
def setCoverRisk(cwetable,selection_name,efficacy_table,budget,rho,Ai,costs):
    # Total CWEs for all layer
    cwe_table = cwetable    # consider all 25 CWEs
    # cwe_table = cwetable.sample(n=20)     # consider a fraction to generate different sol (alt: frac=0.4 to use fraction of table)

    Zn_agg,eZn_agg,Zn_cap_agg,eZn_cap_agg = Zn_data(cwe_table,selection_name,efficacy_table,budget,rho,Ai)

    print(f'Total val: eZn{np.mean(eZn_agg)} - total cost({sum(costs)}) = {np.mean(eZn_agg) - sum(costs)}')
    print(f'Total val: eZn_cap{np.mean(eZn_cap_agg)} - total cost({sum(costs)}) = {np.mean(eZn_cap_agg) - sum(costs)}')

    return(np.mean(Zn_agg),np.mean(eZn_agg),np.mean(Zn_cap_agg),np.mean(eZn_cap_agg),sum(costs))
