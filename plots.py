import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import itertools
import pandas as pd
plt.style.use('ggplot')
# from sklearn import preprocessing
# import seaborn as sns

# def plot(v,pv_anPDF,pv_anCDF,pv_emp_exp,pv_emp_log,phase):
def plot(v,pv_anPDF,pv_emp_exp,pv_emp_exp_95,phase):
    print(pv_emp_exp_95)
    plt.hist(pv_emp_exp,bins=100,density=True,color='mediumseagreen',alpha=1,label='Simulated PDF')
    # sns.distplot(pv_emp_exp, hist=True, kde=False, bins=100, norm_hist=True)
    plt.plot(v,pv_anPDF,color='darkred',linestyle='dashed',label='Analytical PDF')
    # plt.plot(v,pv_anCDF,'k:',label='Analytical CDF (exponential)')
    # plt.hist(pv_emp_log,bins=100,density=1,color='green',alpha=0.7,label='Simulated PDF (log-norm)')
    plt.axvline(x=pv_emp_exp_95,color='k',label='95% = £{}'.format(pv_emp_exp_95))
    plt.xlabel('Present Value £ '+ '('+phase+')')
    plt.ylabel('Frequency')
    plt.legend(loc='best',fontsize=11)
    # fig.tight_layout()
    plt.show()


def pv_total(pv1,pv2,pv_95,phase):
    plt.hist(pv1,bins=100,density=1,color='blue',alpha=0.6,label='Simulated PDF (exponential)')
    plt.hist(pv2,bins=100,density=1,color='green',alpha=0.7,label='Simulated PDF (log-norm)')
    plt.axvline(x=pv_95,color='k',label='95% = £{}'.format(pv_95))
    plt.xlabel('Present Value £ '+ '('+phase+')')
    plt.ylabel('Frequency')
    plt.legend(loc='best')
    plt.show()


def setCoverPlot(subcontrols_list,position,positionCL,positionCH,positionEL,positionEH):
    no_constraint = [float('nan') for x in range(len(subcontrols_list))]
    costL = [float('nan') for x in range(len(subcontrols_list))]
    costH = [float('nan') for x in range(len(subcontrols_list))]
    cost_efficacyL = [float('nan') for x in range(len(subcontrols_list))]
    cost_efficacyH = [float('nan') for x in range(len(subcontrols_list))]
    for i in position:
        no_constraint[i] = 1
    for i in positionCL:
        costL[i] = 2
    for i in positionCH:
        costH[i] = 3
    for i in positionEL:
        cost_efficacyL[i] = 4
    for i in positionEH:
        cost_efficacyH[i] = 5

    x = np.arange(len(subcontrols_list))
    y = [0,1,2,3,4,5]
    fig, ax = plt.subplots()
    ax.scatter(x,no_constraint,s=70,color='black')
    ax.scatter(x,costL,marker='D',s=60,color='black')
    ax.scatter(x,costH,marker='X',s=60,color='black')
    ax.scatter(x,cost_efficacyL,marker='h',s=80,color='black')
    ax.scatter(x,cost_efficacyH,marker='*',s=90,color='black')
    # plt.axhline(y=1, linestyle=':',color='k',alpha=0.2)
    # plt.axhline(y=2, linestyle=':',color='k',alpha=0.2)
    # plt.axhline(y=3, linestyle=':',color='k',alpha=0.2)
    # plt.axhline(y=4, linestyle=':',color='k',alpha=0.2)
    # plt.axhline(y=5, linestyle=':',color='k',alpha=0.2)

    # ax.set_ylabel('Subcontrol Selection with')
    ax.set_yticks(y)
    # ax.set_yticklabels([0,'No Constraint','Cost (Level L)','Cost (Level H)', 'Cost and Efficacy\n(Level L,eff=0.015)', 'Cost and Efficacy\n(Level H,eff=0.015)'])
    # ax.text(s='Cost and Efficacy\n(Level L)', x=-6, y=3.7)
    # ax.text(s='Cost and Efficacy\n(Level H)', x=-12.2, y=4.7)
    ax.set_yticklabels([0,'A','B','C','D','E'])
    ax.text(-1, -3, "(A) no constraint. (B) budget constraint for subcontrols level L. (C) budget constraint for subcontrols level H. (D) budget and efficacy bound for subcontrols level L. (E) budget and efficacy bound for subcontrols level H.", color='black', wrap=True,
        bbox=dict(facecolor='none', edgecolor='black', pad=10.0))

    ax.set_xlabel('CIS Subcontrols')
    # ax.set_title('Set Cover Problem Control Selection')
    ax.set_xticks(x)
    ax.set_xticklabels(subcontrols_list, rotation=90)
    fig.tight_layout()
    plt.show()


def setCoverEfficacyBoundPlot(subcontrols_list,efficacy_bound,pos_EL,pos_EH):
    cost_efficacyL = [[float('nan') for x in range(len(subcontrols_list))] for x in range(len(pos_EL))]
    cost_efficacyH = [[float('nan') for x in range(len(subcontrols_list))] for x in range(len(pos_EH))]
    efficacy_bound.insert(0,0)
    for i in range(len(pos_EL)):
        if i == 0:
            for x in pos_EL[i]:
                cost_efficacyL[i][x] = 1
            for y in pos_EH[i]:
                cost_efficacyH[i][y] = 1
        elif i == 1:
            for x in pos_EL[i]:
                cost_efficacyL[i][x] = 2
            for y in pos_EH[i]:
                cost_efficacyH[i][y] = 2
        elif i == 2:
            for x in pos_EL[i]:
                cost_efficacyL[i][x] = 3
            for y in pos_EH[i]:
                cost_efficacyH[i][y] = 3
        elif i == 3:
            for x in pos_EL[i]:
                cost_efficacyL[i][x] = 4
            for y in pos_EH[i]:
                cost_efficacyH[i][y] = 4

    x = np.arange(len(subcontrols_list))
    y = np.arange(len(efficacy_bound))
    fig, ax = plt.subplots()
    for i in range(len(cost_efficacyL)):
        L = ax.scatter(x,cost_efficacyL[i],s=70,color='steelblue')
        H = ax.scatter(x,cost_efficacyH[i],marker='x',s=60,color='black')
        # plt.axhline(y=i+1, linestyle=':',color='k',alpha=0.2)

    ax.set_ylabel('Efficacy Bound')
    ax.set_yticks(y)
    ax.set_yticklabels(efficacy_bound)
    ax.set_xlabel('CIS Subcontrols')
    # ax.set_title('Set cover control selection with cost and efficacy bounds')
    ax.set_xticks(x)
    ax.set_xticklabels(subcontrols_list, rotation=90)
    plt.legend((L, H), ('Level L', 'Level H'), scatterpoints=1)
    fig.tight_layout()
    plt.show()


def knapsackOptimisationPlot(subcontrols_list,position,levels):
    kp_selection = [float('nan') for x in range(len(subcontrols_list))]
    for (i,j) in zip(position,levels):
        if j == 0:
            kp_selection[i] = 1
        else:
            kp_selection[i] = 2

    x = np.arange(len(subcontrols_list))
    y = [0,1,2]
    fig, ax = plt.subplots()
    ax.bar(x,kp_selection,color="lightseagreen",alpha=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels([0,'Level L','Level H'])
    ax.set_xlabel('CIS Subcontrols')
    ax.set_xticks(x)
    ax.set_xticklabels(subcontrols_list,rotation=90)

    fig.tight_layout()
    plt.show()


def riskPlot(risk_noconstraint,risk_CL,risk_CH,risk_EL,risk_EH,risk_KP,budget):

    figure, axes = plt.subplots(1, 3)
    '''ROSI'''
    rosi = []
    rosi.append((risk_noconstraint[1]-risk_noconstraint[3]-risk_noconstraint[4])/risk_noconstraint[4])
    rosi.append((risk_CL[1]-risk_CL[3]-risk_CL[4])/risk_CL[4])
    rosi.append((risk_CH[1]-risk_CH[3]-risk_CH[4])/risk_CH[4])
    rosi.append((risk_EL[1]-risk_EL[3]-risk_EL[4])/risk_EL[4])
    rosi.append((risk_EH[1]-risk_EH[3]-risk_EH[4])/risk_EH[4])
    rosi.append((risk_KP[1]-risk_KP[3]-risk_KP[4])/risk_KP[4])
    # df = pd.DataFrame({'eZn^':[risk_noconstraint[3],risk_CL[3],risk_CH[3],risk_EL[3],risk_EH[3]], 'Cost':[risk_noconstraint[4],risk_CL[4],risk_CH[4],risk_EL[4],risk_EH[4]], 'ROSI':rosi})
    df1 = pd.DataFrame({'ROSI':rosi})
    ax = df1.plot(kind="barh",ax=axes[2],color={"steelblue"})
    ax.set_yticklabels(['A','B','C','D','E','F'])
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
    ax.legend(loc='upper center',bbox_to_anchor=(0.5,-0.09),fancybox=True,shadow=True,ncol=1,prop={'size': 9})

    '''Risk reduction vs cost'''
    risk_reduction = []
    risk_reduction.append((risk_noconstraint[1]-risk_noconstraint[3]))
    risk_reduction.append((risk_CL[1]-risk_CL[3]))
    risk_reduction.append((risk_CH[1]-risk_CH[3]))
    risk_reduction.append((risk_EL[1]-risk_EL[3]))
    risk_reduction.append((risk_EH[1]-risk_EH[3]))
    risk_reduction.append((risk_KP[1]-risk_KP[3]))
    cost = [risk_noconstraint[4],risk_CL[4],risk_CH[4],risk_EL[4],risk_EH[4],risk_KP[4]]


    # df = pd.DataFrame({'Residual Risk':risk_reduction})
    df2 = pd.DataFrame({'Residual Expected Impact':[risk_noconstraint[3],risk_CL[3],risk_CH[3],risk_EL[3],risk_EH[3],risk_KP[3]], 'Reduced Expected Impact':risk_reduction})
    ax = df2.plot(kind="barh",stacked=True,ax=axes[0],color={"indianred","black"})
    ax.set_yticklabels(['A','B','C','D','E','F'])
    ax.text(0, -3.5, "(A) Set cover with no constraint. (B) Set cover with budget constraint for subcontrols level L. (C) Set cover with budget constraint for subcontrols level H. (D) Set cover with budget and efficacy bound for subcontrols level L. (E) Set cover with budget and efficacy bound for subcontrols level H. (F) Knapsack Optimisation with budget", color='black', wrap=True,
        bbox=dict(facecolor='none', edgecolor='black', pad=5.0), fontsize=10)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])

    # Put a legend below current axis
    ax.legend(loc='upper center',bbox_to_anchor=(0.5,-0.09),fancybox=True,shadow=True,ncol=1,prop={'size': 9})

    df3 = pd.DataFrame({'Cost':cost})
    ax = df3.plot(kind="barh",ax=axes[1],color={"gray"})
    ax.axvline(x=budget, linestyle=':',color='k',alpha=0.2,label='Budget = £'+str(budget))
    ax.set_yticklabels(['A','B','C','D','E','F'])
    # ax.set_xlabel('Budget='+str(budget),fontsize=10)
    # ax.text(budget-10,-0.8,budget)
    # ax.text(-1.4, -2.8, "(A) Set cover with no constraint. (B) Set cover with budget constraint for subcontrols level L. (C) Set cover with budget constraint for subcontrols level H. (D) Set cover with budget and efficacy bound for subcontrols level L. (E) Set cover with budget and efficacy bound for subcontrols level H. (F) Knapsack Optimisation with budget", color='black', wrap=True,
        # bbox=dict(facecolor='none', edgecolor='black', pad=10.0))
    # ax.get_legend()
    # plt.legend()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
    ax.legend(loc='upper center',bbox_to_anchor=(0.5,-0.09),fancybox=True,shadow=True,ncol=1,prop={'size': 9})

    plt.show()


def knapsackRiskPlot(risk_KP_list,budget_list):
    eZn = []
    eZn_cap = []
    cost = []
    rosi = []
    reduced_risk = []
    for i in risk_KP_list:
        eZn.append(i[1])
        eZn_cap.append(i[3])
        cost.append(i[4])
        rosi.append((i[1]-i[3]-i[4])/i[4])
        reduced_risk.append(i[1]-i[3])

    print(f'eZn_cap:{eZn_cap}')
    print(f'rosi:{rosi}')

    # df = pd.DataFrame({'eZn_cap':eZn_cap})
    # ax = df.plot.line(color={"indianred"})
    # plt.plot(budget_list,eZn_cap,color='indianred',label='residual')
    plt.plot(budget_list,rosi,color='steelblue',label='rosi')
    plt.plot(budget_list,reduced_risk,color='black',label='Reduced Expected Impact')
    plt.xlabel('Budget')

    # fig.tight_layout()
    plt.legend(loc='best')
    plt.show()
