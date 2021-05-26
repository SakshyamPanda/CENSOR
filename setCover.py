import time
import numpy as np
from knapsackOptimisation import expectedZn

# Set Cover problem with cost and efficacy constraint
def setCoverCostEfficacy(sets,set_reminder,budget,weights,efficacy,efficacy_bound):
    def setCover(sets,set_reminder,budget,weights,efficacy,efficacy_bound):
        min_element = -1
        for i,s in enumerate(sets):
            if len(s.intersection(set_reminder)) > 0:
                try:
                    cost = weights[i]/(len(s.intersection(set_reminder)))
                    if cost < budget and all(j >= efficacy_bound for j in efficacy[i]):
                        budget = cost
                        min_element = i
                except:
                    pass
        return(sets[min_element],weights[min_element],min_element)

    cover = []
    costs = []
    pos = []
    timeout = time.time() + 60*0.1  # 6 seconds from now
    while len(set_reminder) != 0:
        if time.time() > timeout:
            break
        set_i, cost_i, loc = setCover(sets,set_reminder,budget,weights,efficacy,efficacy_bound)
        if loc != -1:
            cover.append(set_i)
            set_reminder = set_reminder.difference(set_i)
            costs.append(cost_i)
            pos.append(loc)
        time.sleep(1)
    print(f'{cover}---{sum(costs)},{costs}----{pos}')
    return(cover,costs,pos)


# Set Cover with cost constraint
def setCoverCost(sets,set_reminder,budget,weights):
    def setCover(sets,set_reminder,budget,weights):
        min_element = -1
        for i,s in enumerate(sets):
            if len(s.intersection(set_reminder)) > 0:
                try:
                    cost = weights[i]/(len(s.intersection(set_reminder)))
                    if cost < budget:
                        budget = cost
                        min_element = i
                except:
                    pass
        return(sets[min_element],weights[min_element],min_element)

    cover = []
    costs = []
    pos = []
    timeout = time.time() + 60*0.1  # 6 seconds from now
    while len(set_reminder) != 0:
        if time.time() > timeout:
            break
        set_i, cost_i, loc = setCover(sets,set_reminder,budget,weights)
        if loc != -1:
            cover.append(set_i)
            set_reminder = set_reminder.difference(set_i)
            costs.append(cost_i)
            pos.append(loc)
        time.sleep(1)
    print(f'{cover}---{sum(costs)},{costs}----{pos}')
    return(cover,costs,pos)


# Set Cover Problem with No Constraint
def setCover(sets,set_reminder,costH):
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
    print(f'{cover}---{pos}')
    costs = [costH[i] for i in pos]
    return(cover,costs,pos)

# Set Cover Problem risk (E[Zn]) calculation
def setCoverRisk(cwetable,selection_name,efficacy_table,budget,rho,Ai,costs):
    # Total CWEs for all layer
    cwe_table = cwetable    # consider all 25 CWEs
    # cwe_table = cwetable.sample(n=20)     # consider a fraction to generate different sol (alt: frac=0.4 to use fraction of table)

    # extracting the efficacy
    # eff = efficacy_table.loc[efficacy_table['CWE'].isin(list(cwe_table['CWE']))]

    Zn_agg = []
    eZn_agg = []
    Zn_cap_agg = []
    eZn_cap_agg = []
    # 100 rounds
    for n in range(1):
        # Ri for each layer
        Ri = []
        Si = []
        Si_cap = []
        RiSi = []
        RiSi_cap = []
        time_list = []
        cwe_layer = []
        selection_eff_product = []
        for i in range(len(Ai)):
            cwe_layer.append(cwe_table.sample(n=25))
            cwe_list = list(cwe_layer[i]['CWE'])
            # print(cwe_layer[i]['CWE'])
            cwe_subcontrol = efficacy_table.loc[efficacy_table['CWE'].isin(list(cwe_layer[i]['CWE'])), selection_name]
            selection_eff_product.append(list(cwe_subcontrol.product(axis=1)))
            # effi = [1-x for x in selection_eff_product[i]]

            Ri.append(list(cwe_layer[i]['NormalisedAvg_CVSS_V3_exploitabilityScore']))
            Si.append(list(cwe_layer[i]['NormalisedAvg_CVSS_V3_attackComplexity']))
            RiSi.append(round(np.inner(Ri[i],Si[i]),3))
            Si_cap.append(np.multiply(Si[i],selection_eff_product[i]))
            RiSi_cap.append(round(np.inner(Ri[i],Si_cap[i]),3))
            time_list.append(round(cwe_layer[i]['Avg_CVSS_V3_time'].mean(),3))

        # print(cwe_layer)
        # print(f'Si: {Si}')
        # print(f'sel_prod: {selection_eff_product}')
        # print(f'Si_cap: {Si_cap}')
        # print(f'RiSi:{RiSi}')
        # print(f'RiSi_cap:{RiSi_cap}')

        Zn, eZn = expectedZn(Ai,RiSi,time_list,rho)
        Zn_cap, eZn_cap = expectedZn(Ai,RiSi_cap,time_list,rho)
        Zn_agg.append(sum(Zn))
        eZn_agg.append(sum(eZn))
        Zn_cap_agg.append(sum(Zn_cap))
        eZn_cap_agg.append(sum(eZn_cap))

    print(f'Total val: eZn{np.mean(eZn_agg)} - total cost({sum(costs)}) = {np.mean(eZn_agg) - sum(costs)}')
    print(f'Total val: eZn_cap{np.mean(eZn_cap_agg)} - total cost({sum(costs)}) = {np.mean(eZn_cap_agg) - sum(costs)}')

    return(np.mean(Zn_agg),np.mean(eZn_agg),np.mean(Zn_cap_agg),np.mean(eZn_cap_agg),sum(costs))
