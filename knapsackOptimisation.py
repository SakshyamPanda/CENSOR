import pandas as pd
import numpy as np
import itertools
import json
import math
from pdf_calculation import PDFCalculation

def dynamicKnapsack(controls_pair,cost_matrix,eff_prod,budget):
    n = len(controls_pair)
    efficacy_matrix = [eff_prod[i:i+2] for i in range(0, len(eff_prod), 2)]
    knapsack_matrix = [[0 for x in range(budget+1)] for x in range(len(controls_pair)+1)]
    for j in range(n+1):
        for c in range(budget+1):
            if j == 0 or c == 0:
                knapsack_matrix[j][c] = 0
            else:
                knapsack_matrix[j][c] = knapsack_matrix[j-1][c]
                for i in range(2):
                    if c >= (cost_matrix[j-1][i][0]):
                        knapsack_matrix[j][c] = max(knapsack_matrix[j][c],(knapsack_matrix[j-1][c-math.ceil(cost_matrix[j-1][i][0])]+(efficacy_matrix[j-1][i])))

    res = knapsack_matrix[n][budget]
    w = budget
    sol = []
    total_cost = []
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == knapsack_matrix[i-1][w]:
            continue
        else:
            max_value = max(efficacy_matrix[i-1])
            max_index = efficacy_matrix[i-1].index(max_value)
            min_value = min(efficacy_matrix[i-1])
            min_index = efficacy_matrix[i-1].index(min_value)
            if  cost_matrix[i-1][max_index][0] <= w:
                sol.append((i-1,max_index, max_value))
                res = res - max_value
                w = w - math.ceil(cost_matrix[i-1][max_index][0])
                total_cost.append(cost_matrix[i-1][max_index][0])
            elif cost_matrix[i-1][min_index][0] <= w:
                sol.append((i-1,min_index, min_value))
                res = res - min_value
                w = w - math.ceil(cost_matrix[i-1][min_index][0])
                total_cost.append(cost_matrix[i-1][min_index][0])
            else:
                continue
    print(f'KP matrix[n][B]: {knapsack_matrix[n][budget]}')
    print(f'control,level,optimised_eff --> {sol}') # sum of optimised_eff == knapsack_matrix[n][B] (last cell)
    print(f'total cost:{sum(total_cost)}----{total_cost}')
    return(sol,total_cost)

def expectedZn(Ai,RiSi,lambda_list,rho):
    n = len(Ai)
    coeff = []
    Zn = []
    temp_lambda = np.zeros(shape=(n,n))
    for i in range(n):
        coeff.append(lambda_list[i]/(lambda_list[i]+rho))
        for j in range(n):
            if j == i or lambda_list[j]-lambda_list[i] == 0:
                temp_lambda[i][j] = 1
            else:
                temp_lambda[i][j] = abs(float(lambda_list[j]/(lambda_list[j]-lambda_list[i])))
    lambda_product = np.multiply.reduce(temp_lambda,axis=1)
    print(f'lambda_product:{lambda_product}')
    Zn = []
    eZn = []
    for i in range(n):
        Zn.append(round(Ai[i]*RiSi[i],5))
        eZn.append(round(Ai[i]*RiSi[i]*coeff[i]*lambda_product[i],5))
    print(f'Zn: {Zn}---{sum(Zn)}')
    print(f'eZn: {eZn}---{sum(eZn)}')
    return(Zn,eZn)


def Zn_data(cwe_table,selection_name,efficacy_table,budget,rho,Ai):
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
            # cwe_layer.append(cwe_table.sample(n=5))
            if i == 0:
                cwe_layer.append(pd.DataFrame(cwe_table.iloc[:(i+1)*8,:]))
            elif i == 1:
                cwe_layer.append(pd.DataFrame(cwe_table.iloc[8:(i+1)*8,:]))
            else:
                cwe_layer.append(pd.DataFrame(cwe_table.iloc[16:,:]))
            cwe_list = list(cwe_layer[i]['CWE'])
            cwe_subcontrol = efficacy_table.loc[efficacy_table['CWE'].isin(list(cwe_layer[i]['CWE'])), selection_name]
            selection_eff_product.append(list(cwe_subcontrol.product(axis=1)))
            effi = [1-x for x in selection_eff_product[i]]

            Ri.append(list(cwe_layer[i]['NormalisedAvg_CVSS_V3_exploitabilityScore']))
            Si.append(list(cwe_layer[i]['NormalisedAvg_CVSS_V3_attackComplexity']))
            RiSi.append(round(np.inner(Ri[i],Si[i]),5))
            Si_cap.append(np.multiply(Si[i],effi))
            RiSi_cap.append(round(np.inner(Ri[i],Si_cap[i]),5))
            time_list.append(round(cwe_layer[i]['Avg_CVSS_V3_time'].mean(),5))

        lambda_list = [1/i for i in time_list]
        Zn, eZn = expectedZn(Ai,RiSi,lambda_list,rho)
        Zn_cap, eZn_cap = expectedZn(Ai,RiSi_cap,lambda_list,rho)
        Zn_agg.append(sum(Zn))
        eZn_agg.append(sum(eZn))
        Zn_cap_agg.append(sum(Zn_cap))
        eZn_cap_agg.append(sum(eZn_cap))

    # Calculating PDF
    PDFCalculation(lambda_list,rho,eZn_cap)
    return(Zn_agg,eZn_agg,Zn_cap_agg,eZn_cap_agg)


# This is the main function here
def knapsackOptimisation(cwetable,efficacy_table,cost_table,mapping_table,budget,rho,Ai):
    # Total CWEs for all layer
    cwe_table = cwetable    # consider all 25 CWEs
    # cwe_table = cwetable.sample(n=20)     # consider a fraction to generate different sol (alt: frac=0.4 to use fraction of table)

    # extracting the efficacy
    eff = efficacy_table.loc[efficacy_table['CWE'].isin(list(cwe_table['CWE']))]
    controls = list(cost_table.columns)
    eff_prod = []
    for col in controls:
        eff_prod.append(eff[col].product())

    # list of list
    controls_pair = [[controls[i],controls[i+1]] for i in range(0,len(controls),2)]
    cost_matrix = [[0 for x in range(2)] for x in range(len(controls_pair))]
    for i,con in enumerate(controls_pair):
        for j,c in enumerate(con):
            cost_matrix[i][j] = list(cost_table[c])

    selection,costs = dynamicKnapsack(controls_pair,cost_matrix,eff_prod,budget)

    subcontrols_selected = []
    subcontrols_level = []
    selection_name = []
    selection_eff_product = []
    for i in selection:
        selection_name.append(controls_pair[i[0]][i[1]])
        subcontrols_selected.append(i[0])
        subcontrols_level.append(i[1])

    print(f'selection_name:{selection_name}')
    Zn_agg,eZn_agg,Zn_cap_agg,eZn_cap_agg = Zn_data(cwe_table,selection_name,efficacy_table,budget,rho,Ai)

    # Mean of Zn and eZn is required if we run more than 1 iterations
    print(f'Total val: eZn {eZn_agg},{np.mean(eZn_agg)} - total cost({sum(costs)}) = {np.mean(eZn_agg) - sum(costs)}')
    print(f'Total val: eZn_cap {eZn_cap_agg},{np.mean(eZn_cap_agg)} - total cost({sum(costs)}) = {np.mean(eZn_cap_agg) - sum(costs)}')

    return(subcontrols_selected,subcontrols_level,sum(costs),np.mean(Zn_agg),np.mean(eZn_agg),np.mean(Zn_cap_agg),np.mean(eZn_cap_agg))
