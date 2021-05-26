# from ortools.linear_solver import pywraplp
import numpy as np
import pandas as pd
from setCover import setCover, setCoverCost, setCoverCostEfficacy, setCoverRisk
from knapsackOptimisation import knapsackOptimisation
from plots import setCoverPlot, setCoverEfficacyBoundPlot, knapsackOptimisationPlot, riskPlot

# Reading data tables
efficacy_table = pd.read_csv('data/control_efficacy_table.csv')
cost_table = pd.read_csv('data/control_cost_table.csv')
mapping_table = pd.read_excel('data/cwe-cisIG1-mapping_v2.xlsx') #engine='openpyxl'
mapping_table = mapping_table.dropna(axis='columns')
mapping_table = mapping_table.loc[:,(mapping_table != 0).any(axis=0)]
cwe_table = pd.read_csv('data/top_25_CWE_table.csv')
cwe = list(mapping_table['CWE'])

'''Creating sets for Set Cover Problem'''
universe = set([i for i in range(len(mapping_table['CWE']))])
sets = []
efficacyL = []
efficacyH = []
subcontrols = list(mapping_table.columns[2:])
for ind,col in enumerate(subcontrols):
    '''Creating set as each column of mapping table (subcontrol addressing CWEs)'''
    col_value = list(mapping_table[col])
    control_temp = set([i for i, e in enumerate(col_value) if e != 0])
    sets.append(control_temp)
    '''Saperating efficacies of L and H'''
    controlL = str(col) + str('_L')
    controlH = str(col) + str('_H')
    efficacyL.append(list(efficacy_table[controlL]))
    efficacyH.append(list(efficacy_table[controlH]))

costL = [cost_table.iat[0,i] for i in range(0,len(cost_table.columns),2)]
costH = [cost_table.iat[0,i] for i in range(1,len(cost_table.columns),2)]

set_reminder = universe
budget = 120
rho = 0.3
Ai = [1,2,3]
efficacy_bound = 0.020


if __name__ == '__main__':

    ####### SET 1
    ''' Set Cover problem with no weights '''
    covers, costs, position = setCover(sets,set_reminder,costH)
    for i in position:
        print(subcontrols[i])
    print(f'costs:----{costs}')

    ''' Set Cover problem with cost constraint '''
    ''' For Level L '''
    coversCL, costsCL, positionCL = setCoverCost(sets,set_reminder,budget,costL)
    ''' For Level H '''
    coversCH, costsCH, positionCH = setCoverCost(sets,set_reminder,budget,costH)

    ''' Set Cover problem with cost and efficacy constraint '''
    ''' For Level L '''
    coversEL, costsEL, positionEL = setCoverCostEfficacy(sets,set_reminder,budget,costL,efficacyL,efficacy_bound)
    ''' For Level H '''
    coversEH, costsEH, positionEH = setCoverCostEfficacy(sets,set_reminder,budget,costH,efficacyH,efficacy_bound)

    selection_name_noconstraint = [str(subcontrols[i])+str('_H') for i in position]
    selection_name_CL = [str(subcontrols[i])+str('_L') for i in positionCL]
    selection_name_CH = [str(subcontrols[i])+str('_H') for i in positionCH]
    selection_name_EL = [str(subcontrols[i])+str('_L') for i in positionEL]
    selection_name_EH = [str(subcontrols[i])+str('_H') for i in positionEH]
    # print(efficacyL)

    '''Risk with no contraint'''
    risk_noconstraint = list(setCoverRisk(cwe_table,selection_name_noconstraint,efficacy_table,budget,rho,Ai,costs))
    risk_CL = list(setCoverRisk(cwe_table,selection_name_CL,efficacy_table,budget,rho,Ai,costsCL))
    risk_CH = list(setCoverRisk(cwe_table,selection_name_CH,efficacy_table,budget,rho,Ai,costsCH))
    risk_EL = list(setCoverRisk(cwe_table,selection_name_EL,efficacy_table,budget,rho,Ai,costsEL))
    risk_EH = list(setCoverRisk(cwe_table,selection_name_EH,efficacy_table,budget,rho,Ai,costsEH))

    print(f'risk_CL: {risk_CL}')
    print(f'risk_EL: {risk_EL}')
    print(f'risk_CH: {risk_CH}')
    print(f'risk_EH: {risk_EH}')
    ''' Plots '''
    # setCoverPlot(subcontrols,position,positionCL,positionCH,positionEL,positionEH)


    ###### SET 2
    # efficacy_bound = [0.015,0.025,0.3,0.5]
    # pos_EL = []
    # pos_EH = []
    # for i in efficacy_bound:
    #     ''' For Level L '''
    #     coversEL, costsEL, positionEL = setCoverCostEfficacy(sets,set_reminder,budget,costL,efficacyL,i)
    #     ''' For Level H '''
    #     coversEH, costsEH, positionEH = setCoverCostEfficacy(sets,set_reminder,budget,costH,efficacyH,i)
    #     pos_EL.append(positionEL)
    #     pos_EH.append(positionEH)

    ''' Plots '''
    # setCoverEfficacyBoundPlot(subcontrols,efficacy_bound,pos_EL,pos_EH)



    ''' Knapsack Optimisation'''
    subcontrols_position,subcontrols_level,costsKP,Zn_KP,eZn_KP,Zn_cap_KP,eZn_cap_KP = knapsackOptimisation(cwe_table,efficacy_table,cost_table,mapping_table,budget,rho,Ai)
    # for (i,j) in zip(subcontrols_position,subcontrols_level):
    #     print(f'{subcontrols[i]},{j}')
    risk_KP = [Zn_KP,eZn_KP,Zn_cap_KP,eZn_cap_KP,costsKP]

    ''' Plots '''
    knapsackOptimisationPlot(subcontrols,subcontrols_position,subcontrols_level)
    riskPlot(risk_noconstraint,risk_CL,risk_CH,risk_EL,risk_EH,risk_KP)
